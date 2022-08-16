from django.shortcuts import render
from .models import Post, Tag
# Create your views here.

def post(request, pk):
    post = Post.objects.get(id=pk)
    tags = post.tags.all()
    context = {
        'post': post,
        'tags': tags,
    }
    return render(request, 'posts/post.html', context)

def posts(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'tags': tags,
    }
    return render(request, 'posts/posts.html', context)

