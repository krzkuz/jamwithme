from django.shortcuts import render, redirect
from .models import Follow, Instrument, Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileForm, InstrumentForm, RegisterUserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .utils import paginate_profiles


def register_user(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
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
    follow = Follow.objects.get(user=profile)
    followers = follow.follower.all()
    following = Follow.objects.filter(follower=profile)

    context = {
        'profile': profile,
        'posts': posts,
        'skills': skills,
        'followers': followers,
        'following': following,
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url="login")
def user_settings(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.profile.id)

    context = {
        'form': form
    }
    return render(request, 'users/settings.html', context)

@login_required(login_url="login")
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

@login_required(login_url="login")
def follow(request, pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=user)
    follow.follower.add(request.user.profile)
    return redirect('profile', pk)

@login_required(login_url="login")
def unfollow(request, pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=user)
    follow.follower.remove(request.user.profile)
    return redirect('profile', pk)

def followers(request, pk):
    profile = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=profile)
    followers = follow.follower.all()

    context = {
        'profile': profile,
        'followers': followers,
    }
    return render(request, 'users/followers.html', context)

def following(request, pk):
    profile = Profile.objects.get(id=pk)
    following = Follow.objects.filter(follower=profile)
   
    context = {
        'profile': profile,
        'following': following,
    }
    return render(request, 'users/following.html', context)

def profiles(request):
    profile = request.user.profile
    following = Follow.objects.filter(follower=profile)
    following_profiles = [] 

    for follow in following:
        following_profiles.append(follow.user)
    
    search = request.GET.get('q')
    if search:
        profiles = Profile.objects.distinct().filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    else:
        profiles = Profile.objects.all()
    
    custom_range, profiles = paginate_profiles(request, profiles, 1)
    page = ''
    
    context = {
        'profiles': profiles,
        'page': page,
        'custom_range': custom_range,
        'following_profiles': following_profiles,
        'search': search,
    }
    return render(request, 'users/profiles.html', context)
