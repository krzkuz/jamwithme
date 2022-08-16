from django.shortcuts import render, redirect
from .models import Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('posts')

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            messages.error(request, 'User not found')
    context = {

    }
    return render(request, 'users/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('posts')

# def user_account(request):
#     profile = request.user.profile
#     posts = Post.objects.filter(author=profile)
#     context = {
#         'profile': profile,
#         'posts': posts,
#     }
#     return render(request, 'users/profile.html', context)

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    posts = Post.objects.filter(author=profile)
    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)