from django.shortcuts import render, redirect

from users.models import Follow, Profile
from .models import Post, Tag, Comment, Rate
from .forms import PostForm
from django.db.models import Q
# Create your views here.

def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    comments = Comment.objects.filter(post=post)
    post_rates = Rate.objects.filter(post=post)
    # comment_rates = Rate.objects.filter()
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'post_rates': post_rates,
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
    # if request.user.is_authenticated:
    #     friends = request.user.profile.friend.all()
    # else:
    #     friends = None
    if request.user.is_authenticated:
        profile = request.user.profile
        followed = profile.follower.all()
    else:
        followed = None
    context = {
        'posts': posts,
        'tags': tags,
        'followed': followed,
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
