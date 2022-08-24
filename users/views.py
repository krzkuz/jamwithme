from django.shortcuts import render, redirect
from .models import Instrument, Message, Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileForm, InstrumentForm
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

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    posts = Post.objects.filter(author=profile)
    skills = Instrument.objects.filter(player=profile)
    context = {
        'profile': profile,
        'posts': posts,
        'skills': skills,
    }
    return render(request, 'users/profile.html', context)

def user_settings(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.profile.id)
    context = {
        'form': form
    }
    return render(request, 'users/settings.html', context)

def user_skill(request):
    profile = Profile.objects.get(user=request.user)
    form = InstrumentForm()
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.player = request.user.profile
            skill.save()
            return redirect('profile', request.user.profile.id)
    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)




# def users_messages(request):
#     users_messages = Message.objects.filter()