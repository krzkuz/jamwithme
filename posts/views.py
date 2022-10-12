from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from users.models import Follow, Profile
from .models import Post, Tag, Comment
from .forms import PostForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import paginate_comments, paginate_posts

def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    comments = Comment.objects.filter(post=post)
    likes = post.likes.all()
    dislikes = post.dislikes.all()
    custom_range, comments = paginate_comments(request, comments, 5)

    if request.method == 'POST':
        Comment.objects.get_or_create(
            author=request.user.profile,
            post=post,
            body=request.POST.get('comment')
            )
        return redirect('post', pk)
        # comment.save()

    # post_rates = Rate.objects.filter(post=post)
    # comment_rates = Rate.objects.filter()
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes,
        'custom_range': custom_range,
        # 'form': form,
        # 'post_rates': post_rates,
    }
    return render(request, 'posts/post.html', context)

def posts(request):
    tag = request.GET.get('q')
    if tag:
        tags_filtered = Tag.objects.filter(name=tag)
        posts = Post.objects.distinct().filter(
            Q(body__icontains=tag) |
            Q(subject__icontains=tag) |
            Q(tags__in=tags_filtered)
        )
    else:
        posts = Post.objects.all()
    tags = Tag.objects.all()

    tag_dict = {}
    for tag_search in tags:
        tag_dict[tag_search.name] = tag_search.post_set.all().count()
    # tag_dict.order_by()
    print(tag_dict, '++++++')

    user_id = request.GET.get('u')
    if user_id:
        author = Profile.objects.get(id=user_id)
        posts = author.post_set.all()
    
    if request.user.is_authenticated:
        profile = request.user.profile
        following = profile.follower.all()
    else:
        following = None
    
    custom_range, posts = paginate_posts(request, posts, 1)

    context = {
        'posts': posts,
        'tags': tags,
        'following': following,
        'custom_range': custom_range,
        'tag_dict': tag_dict,
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
            tags.delete()
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
    # post = Post.objects.get(id=pk)
    # if request.user.profile in post.dislikes.all():
    #     post.dislikes.remove(request.user.profile)
    # if request.user.profile in post.likes.all():
    #     post.likes.remove(request.user.profile)
    # else:
    #     post.likes.add(request.user.profile)
    # return redirect('post', pk)

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

# def dislike_post(request, pk):
#     post = Post.objects.get(id=pk)
#     if request.user.profile in post.likes.all():
#         post.likes.remove(request.user.profile)
#     if request.user.profile in post.dislikes.all():
#         post.dislikes.remove(request.user.profile)
#     else:
#         post.dislikes.add(request.user.profile)
#     return redirect('post', pk)

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

# @login_required(login_url="login")
# def delete_comment(request, pk):
#     comment = Comment.objects.get(id=pk)
