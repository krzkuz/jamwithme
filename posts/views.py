from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from users.models import Follow, Profile
from .models import Post, Tag, Comment
from .forms import PostForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import paginate_comments, paginate_posts
from .utils import post_search

def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    comments = Comment.objects.filter(post=post)
    likes = post.likes.all()
    dislikes = post.dislikes.all()
    custom_range, comments = paginate_comments(request, comments, 10)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.get('comment'):
                Comment.objects.get_or_create(
                    author=request.user.profile,
                    post=post,
                    body=request.POST.get('comment')
                    )
                return redirect('post', pk)
    
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes,
        'custom_range': custom_range,
    }
    return render(request, 'posts/post.html', context)

def posts(request):
    posts = Post.objects.all()
    posts, search = post_search(request, posts)
    tags = Tag.objects.all()

    # following user posts
    user_id = request.GET.get('u')
    if user_id:
        author = Profile.objects.get(id=user_id)
        posts = author.post_set.all()
    else:
        author = None
        
    popular_tags = {}
    for tag in tags:
        popular_tags[tag.name] = tag.post_set.all().count()
    popular_tags = sorted(popular_tags.items(), key=lambda x: x[1], reverse=True)
    popular_tags = popular_tags[:10] 
    popular_tags = dict(popular_tags)
    
    
    if request.user.is_authenticated:
        profile = request.user.profile
        following = profile.follower.all()
    else: 
        following = None
    
    custom_range, posts = paginate_posts(request, posts, 10)

    context = {
        'posts': posts,
        'tags': tags,
        'following': following,
        'custom_range': custom_range,
        'popular_tags': popular_tags,
        'search': search,
        'user_search': author,
    }
    return render(request, 'posts/posts.html', context)

@login_required(login_url="login")
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            get_tags = request.POST.get('tags').replace(',', ' ').split()
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            for tag in get_tags:
                tag, created = Tag.objects.get_or_create(name=tag.lower().capitalize())
                post.tags.add(tag)
            
            return redirect('posts') 
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)

@login_required(login_url="login")
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    tags = post.tags.all()
    str_tags = ''
    for tag in tags:
        str_tags += str(tag.name) + ' '
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            get_tags = request.POST.get('tags').replace(',', ' ').split()
            post = form.save(commit=False)
            post.save()

            for tag in tags:
                post.tags.remove(tag)
            # post.tags.all().delete()
            if get_tags:
                for tag in get_tags:
                    tag, created = Tag.objects.get_or_create(name=tag.lower().capitalize())
                    post.tags.add(tag)        
            return redirect('post', pk)
    context = {
        'form': form,
        'tags': str_tags,
    }
    return render(request, 'posts/create_post.html', context)

@login_required(login_url="login")
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete() 
        return redirect('posts')
    context = {
        'post': post
    }
    return render(request, 'posts/delete_post.html', context)

@login_required(login_url="login")
def like_post(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('postid')
        post = get_object_or_404(Post, id=id)
        if request.user.profile in post.dislikes.all():
            post.dislikes.remove(request.user.profile)
        if request.user.profile in post.likes.all():
            post.likes.remove(request.user.profile)
            liked = False
        else:
            post.likes.add(request.user.profile)
            liked = True
        dislikes = post.dislikes.all().count()
        likes = post.likes.all().count()

        return JsonResponse({
            'likes': likes,
            'dislikes': dislikes,
            # 'liked': liked,
         })

@login_required(login_url="login")
def dislike_post(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('postid')
        post = get_object_or_404(Post, id=id)
        if request.user.profile in post.likes.all():
            post.likes.remove(request.user.profile)
        if request.user.profile in post.dislikes.all():
            post.dislikes.remove(request.user.profile)
            # liked = False
        else:
            post.dislikes.add(request.user.profile)
            # liked = True
        dislikes = post.dislikes.all().count()
        likes = post.likes.all().count()

        return JsonResponse({
            'likes': likes,
            'dislikes': dislikes,
            # 'liked': liked,
         })

# @login_required
# def like_comment(request):
#     if request.POST.get('action') == 'post':
#         id = request.POST.get('postid')
#         comment = get_object_or_404(Comment, id=id)
#         if request.user.profile in comment.dislikes.all():
#             comment.dislikes.remove(request.user.profile)
#         if request.user.profile in comment.likes.all():
#             comment.likes.remove(request.user.profile)
#             liked = False
#         else:
#             comment.likes.add(request.user.profile)
#             liked = True
#         dislikes = comment.dislikes.all().count()
#         likes = comment.likes.all().count()

#         return JsonResponse({
#             'likes': likes,
#             'dislikes': dislikes,
#             # 'liked': liked,
#          })

# @login_required
# def dislike_comment(request):
#     if request.POST.get('action') == 'post':
#         id = request.POST.get('postid')
#         comment = get_object_or_404(Comment, id=id)
#         if request.user.profile in comment.likes.all():
#             comment.likes.remove(request.user.profile)
#         if request.user.profile in comment.dislikes.all():
#             comment.dislikes.remove(request.user.profile)
#             # liked = False
#         else:
#             comment.dislikes.add(request.user.profile)
#             # liked = True
#         dislikes = comment.dislikes.all().count()
#         likes = comment.likes.all().count()

#         return JsonResponse({
#             'likes': likes,
#             'dislikes': dislikes,
#             # 'liked': liked,
#          })

@login_required(login_url="login")
def like_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.profile in comment.dislikes.all():
        comment.dislikes.remove(request.user.profile)
    if request.user.profile in comment.likes.all():
        comment.likes.remove(request.user.profile)
    else:
        comment.likes.add(request.user.profile)
    return redirect('post', comment.post.id)

@login_required(login_url="login")
def dislike_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.profile in comment.likes.all():
        comment.likes.remove(request.user.profile)
    if request.user.profile in comment.dislikes.all():
        comment.dislikes.remove(request.user.profile)
    else:
        comment.dislikes.add(request.user.profile)
    return redirect('post', comment.post.id)

@login_required(login_url="login")
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.profile == comment.author:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))
# @login_required(login_url="login")
# def create_comment(request, pk):
#     print('test')
#     if request.method == 'POST':
#         print('test1')
#         if request.user.is_authenticated:
#             print('test2')
#             Comment.objects.get_or_create(
#                 author=request.user.profile,
#                 post=post,
#                 body=request.POST.get('comment')
#                 )
#             print('test3')
#             return redirect('post', pk)
        # elif request.POST.get('rate'):
        #     messages.error(request, 'Login to rate a post')
        #     return redirect('login')
        # else:
        #     messages.error(request, 'Login to add a comment')
        #     return redirect('login')
        

# @login_required(login_url="login")
# def delete_comment(request, pk):
#     comment = Comment.objects.get(id=pk)

# def django_messages(request):
#     if 'comment' in request.POST:
#         next = request.POST.get('next', '/')
#         next = next[1:-1]
#         print(next, '+++++++++')
#         messages.error(request, 'Login to add a comment')
#         return redirect('login', next)
        # else:
        #     messages.error(request, 'Login to rate this post')
        #     return redirect('login')