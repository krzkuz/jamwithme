from django.shortcuts import render, redirect
from .models import Follow, Instrument, Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ProfileForm, InstrumentForm, RegisterUserForm
from django.contrib.auth.decorators import login_required
from .utils import paginate_profiles, profile_search


def register_user(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'You have created an account')
            return redirect('posts')
        else:
            messages.error(request, 'Wrong username or password')

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

def login_user(request):
    if request.POST.get('comments'):
        messages.error(request, 'Login to add a comment')
        return render(request, 'users/login.html')
    if request.POST.get('rate'):
        messages.error(request, 'Login to rate a post')
        return render(request, 'users/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get('next', '/')
            if next:
                return redirect(next)
            else:
                return redirect('posts')
        else:
            messages.error(request, 'User not found')
    return render(request, 'users/login.html')

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
            profile = form.save(commit=False)
            profile.first_name = str(profile.first_name).capitalize()
            profile.last_name = str(profile.last_name).capitalize()
            profile.save()
            return redirect('profile', request.user.profile.id)

    context = {
        'form': form
    }
    return render(request, 'users/settings.html', context)

@login_required(login_url="login")
def user_skill(request):
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
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('profile', pk)

@login_required(login_url="login")
def unfollow(request, pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=user)
    follow.follower.remove(request.user.profile)
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('profile', pk)

@login_required(login_url="login")
def followers(request, pk):
    profile = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=profile)
    followers_obj = follow.follower.all()

    following_obj = Follow.objects.filter(follower=profile)
    following = []
    for obj in following_obj:
        following.append(obj.user)

    followers, search = profile_search(request, followers_obj)
    custom_range, followers = paginate_profiles(request, followers, 10)
    page = ''

    context = {
        'profile': profile,
        'followers': followers,
        'following': following,
        'page': page,
        'custom_range': custom_range,
        'search': search,
    }
    return render(request, 'users/followers.html', context)

@login_required(login_url="login")
def following(request, pk):
    profile = Profile.objects.get(id=pk)   
    following = Follow.objects.filter(follower=profile)
    following_users_ids = []
    for follow in following:
        following_users_ids.append(follow.user.id)
    following = Profile.objects.filter(id__in=following_users_ids)
    following, search = profile_search(request, following)
    
    custom_range, following = paginate_profiles(request, following, 10)
    page = ''


    context = {
        'profile': profile,
        'following': following,
        'page': page,
        'custom_range': custom_range,
        'search': search,
    }
    return render(request, 'users/following.html', context)

@login_required(login_url="login")
def profiles(request):
    profile = request.user.profile
    profiles = Profile.objects.all()
    following = Follow.objects.filter(follower=profile)
    following_profiles = [] 

    for follow in following:
        following_profiles.append(follow.user)
    
    profiles, search = profile_search(request, profiles)
    custom_range, profiles = paginate_profiles(request, profiles, 10)
    page = ''

    context = {
        'profiles': profiles,
        'page': page,
        'custom_range': custom_range,
        'following_profiles': following_profiles,
        'search': search,
    }
    return render(request, 'users/profiles.html', context)
