from django.shortcuts import render, redirect

from users.models import Follow, Profile
from .models import Post, Tag, Comment
from .forms import PostForm
from django.db.models import Q
# Create your views here.

def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    comments = Comment.objects.filter(post=post)
    likes = post.likes.all()
    dislikes = post.dislikes.all()
    # post_rates = Rate.objects.filter(post=post)
    # comment_rates = Rate.objects.filter()
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes,
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
    
    user_id = request.GET.get('u')
    if user_id:
        author = Profile.objects.get(id=user_id)
        posts = author.post_set.all()
    
    if request.user.is_authenticated:
        profile = request.user.profile
        following = profile.follower.all()
    else:
        following = None
    context = {
        'posts': posts,
        'tags': tags,
        'following': following,
    }
    return render(request, 'posts/posts.html', context)

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

def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)

def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {
        'post': post
    }
    return render(request, 'posts/delete_post.html', context)

def like_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.profile in post.dislikes.all():
        post.dislikes.remove(request.user.profile)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    else:
        post.likes.add(request.user.profile)
    return redirect('post', pk)

def dislike_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.profile in post.likes.all():
        post.likes.remove(request.user.profile)
    if request.user.profile in post.dislikes.all():
        post.dislikes.remove(request.user.profile)
    else:
        post.dislikes.add(request.user.profile)
    return redirect('post', pk)

def like_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.profile in comment.dislikes.all():
        comment.dislikes.remove(request.user.profile)
    if request.user.profile in comment.likes.all():
        comment.likes.remove(request.user.profile)
    else:
        comment.likes.add(request.user.profile)
    return redirect('post', comment.post.id)

def dislike_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user.profile in comment.likes.all():
        comment.likes.remove(request.user.profile)
    if request.user.profile in comment.dislikes.all():
        comment.dislikes.remove(request.user.profile)
    else:
        comment.dislikes.add(request.user.profile)
    return redirect('post', comment.post.id)
