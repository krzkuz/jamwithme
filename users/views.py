from django.shortcuts import render, redirect
from .models import Follow, Instrument, Message, Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import MessageForm, ProfileForm, InstrumentForm
from django.db.models import Q
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
    follow = Follow.objects.get(user=profile)
    followers = follow.follower.all()
    context = {
        'profile': profile,
        'posts': posts,
        'skills': skills,
        'followers': followers,
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

def follow(request, pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=user)
    follower = follow.follower.add(request.user.profile)
    # follower = Follow.objects.create(user=user, follower=request.user.profile)
    return redirect('profile', pk)

# def add_friend(request, pk):
#     friend = Profile.objects.get(id=pk)
#     request.user.profile.friend.add(friend)
#     return redirect('profile', pk)

def unfollow(request, pk):
    user = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=user)
    follower = follow.follower.remove(request.user.profile)
    return redirect('profile', pk)

# def delete_friend(request, pk):
#     friend = Profile.objects.get(id=pk)
#     request.user.profile.friend.remove(friend)
#     return redirect('profile', pk)

def followers(request, pk):
    profile = Profile.objects.get(id=pk)
    follow = Follow.objects.get(user=profile)
    followers = follow.follower.all()
    context = {
        'profile': profile,
        'followers': followers,
    }
    return render(request, 'users/followers.html', context)

def users_messages(request):
    profile = Profile.objects.get(user=request.user)
    follow = Follow.objects.get(user=profile)
    following = profile.follower.all()
    followers = follow.follower.all()
    conversations = Message.objects.filter(
        Q(sender=request.user.profile) |
        Q(recipient=request.user.profile)
    )
    context = {
        'following': following,
        'followers': followers,
        'conversations': conversations,
    }
    return render(request, 'users/messages.html', context)

# def users_messages(request):
#     users_messages = Message.objects.filter(
#         Q(sender=request.user.profile) |
#         Q(recipient=request.user.profile)
#     )
#     context = {
#         'users_messages': users_messages,
#     }
#     return render(request, 'users/messages.html', context)

# def message(request, pk):
#     message = Message.objects.get(id=pk)
#     context = {
#         'message': message,
#     }
#     return render(request, 'users/message.html', context)

def send_message(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.recipient = recipient
            message.save()
            return redirect('profile', pk)
    context = {
        'form': form,
    }
    return render(request, 'users/message_form.html', context)