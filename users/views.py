import uuid
from django.shortcuts import render, redirect
from .models import Follow, Instrument, Profile
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import ProfileForm, InstrumentForm, RegisterUserForm
from django.db.models import Q

# Create your views here.

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
    follow.follower.add(request.user.profile)
    # follower = Follow.objects.create(user=user, follower=request.user.profile)
    return redirect('profile', pk)

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
    # following = profile.follow.follower.all()
    following = Follow.objects.filter(follower=profile)
    print(following,'++++++')
    context = {
        'profile': profile,
        'following': following,
    }
    return render(request, 'users/following.html', context)

def profiles(request):
    search = request.GET.get('q')
    if search:
        profiles = Profile.objects.distinct().filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    else:
        profiles = Profile.objects.all()
    page = ''
    
    context = {
        'profiles': profiles,
        'page': page,
    }
    return render(request, 'users/profiles.html', context)

# def users_messages(request, pk):
#     profile = Profile.objects.get(user=request.user)
#     follow = Follow.objects.get(user=profile)
#     following = profile.follower.all()
#     followers = follow.follower.all()
#     last_conversations = Message.objects.filter(
#         Q(sender=request.user.profile) |
#         Q(recipient=request.user.profile)
#     )
#     #conversations = 
#     # Moze zmiana tu
#     # lub response boolean w modelu
#     if pk == 'None':
#         conversation = Message.objects.all().order_by('-created')
#     else:
#         person = Profile.objects.get(id=pk)
#         conversation = Message.objects.filter(
#             Q(sender=person) |
#             Q(recipient=person)
#         ).order_by('-created')
#     context = {
#         'following': following,
#         'followers': followers,
#         'last_conversations': last_conversations,
#         'conversation': conversation,
#     }
#     return render(request, 'users/messages.html', context)

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

# def send_message(request, pk):
#     form = MessageForm()
#     recipient = Profile.objects.get(id=pk)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user.profile
#             message.recipient = recipient
#             message.save()
#             return redirect('profile', pk)
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/message_form.html', context)

# Dzialajace
# def users_messages(request, pk):
#     profile = Profile.objects.get(user=request.user)
#     follow = Follow.objects.get(user=profile)
#     following = profile.follower.all()
#     followers = follow.follower.all()
#     user = Profile.objects.filter(user=request.user)
#     conversations = Conversation.objects.filter(participants__in=user)

#     if pk == 'None':
#         conversation = None
#         room_messages = None
#     else:
#         conversation = Conversation.objects.get(id=pk)
#         room_messages = conversation.message_set.all()

#     form = MessageForm()
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user.profile
#             message.conversation = conversation
#             message.save()
#             return redirect('messages', pk)

#     context = {
#         'following': following,
#         'followers': followers,
#         'conversations': conversations,
#         'room_messages': room_messages,
#         'conversation': conversation,
#         'form': form,
#     }
#     return render(request, 'users/messages.html', context)


# def users_messages(request, pk):
#     profile = Profile.objects.get(user=request.user)
#     follow = Follow.objects.get(user=profile)
#     following = profile.follower.all()
#     followers = follow.follower.all()
#     user = Profile.objects.filter(user=request.user)
#     conversations = Conversation.objects.filter(participants__in=user)
#     participants = user
#     for obj in conversations:
#         participants = participants | obj.participants.all()
#     if pk == 'None':
#         conversation = None
#         room_messages = None
#     else:
#         participant = Profile.objects.get(id=pk)
#         conversation, created = Conversation.objects.get_or_create(id=pk)
#         conversation.participants.add(profile, participant)
#         room_messages = conversation.message_set.all()

#     form = MessageForm()
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user.profile
#             message.conversation = conversation
#             message.save()
#             return redirect('messages', pk)

#     context = {
#         'following': following,
#         'followers': followers,
#         'conversations': conversations,
#         'room_messages': room_messages,
#         'conversation': conversation,
#         'participants': participants,
#         'form': form,
#     }
#     return render(request, 'users/messages.html', context)

# Nie dzialajace

# def users_messages(request, pk):
#     profile = Profile.objects.get(user=request.user)
#     follow = Follow.objects.get(user=profile)
#     following = profile.follower.all()
#     followers = follow.follower.all()
#     user = Profile.objects.filter(user=request.user)
#     conversations = Conversation.objects.filter(participants__in=user)
#     participants = user
#     all_messages = Message.objects.none()

#     # getting queryset of all conversations participants and messages
#     for conversation in conversations:
#         participants = participants | conversation.participants.all()
#         all_messages = all_messages | conversation.message_set.all()
#     if pk == 'None':
#         try:
#             last_message = all_messages.last()
#             conversation = last_message.conversation
#             room_messages = conversation.message_set.all()
#         except:
#             conversation = None
#             room_messages = None
#     else:
#         participant = Profile.objects.get(id=pk)
#         conversation, created = Conversation.objects.get_or_create(id=pk)
#         if created:
#             conversation.id
#         conversation.participants.add(profile, participant)
#         room_messages = conversation.message_set.all()
#         conversation.name = ''
#         i = 1
#         for participant in conversation.participants.all():
#             conversation.name += str(participant.first_name)
#             if i < conversation.participants.all().count():
#                 conversation.name += ', '
#                 i += 1

#         conversation.save()

#     # New message 
#     if conversation:    
#         form = send_message(request, conversation)
#     else:
#         form = None

#     context = {
#         'following': following,
#         'followers': followers,
#         'conversations': conversations,
#         'room_messages': room_messages,
#         'conversation': conversation,
#         'participants': participants,
#         'form': form,
#     }
#     return render(request, 'users/messages.html', context)