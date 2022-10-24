from django.shortcuts import render, redirect
from .models import Message, Conversation
from users.models import Profile, Follow
from .utils import create_conversation, create_conversation_name, profile_search
from django.contrib.auth.decorators import login_required
from users.utils import paginate_profiles

@login_required(login_url="login")
def users_messages(request, pk):
    profile = Profile.objects.get(user=request.user)
    follow = Follow.objects.get(user=profile)
    following = profile.follower.all()
    followers = follow.follower.all()
    user = Profile.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(participants__in=user).order_by('-updated')
    participants = Profile.objects.none()
    all_messages = Message.objects.none()

    # getting queryset of all conversation participants and messages
    for conversation in conversations:
        participants = participants | conversation.participants.all()
        all_messages = all_messages | conversation.message_set.all()
    if pk == 'None':
        try:
            last_message = all_messages.last()
            conversation = last_message.conversation
            room_messages = conversation.message_set.all()
            return redirect('messages', conversation.id)
        except:
            conversation = None
            room_messages = None
    else:
        try:
            participant = Profile.objects.get(id=pk)
            user_conversations = profile.conversation_set.all()
            for obj in user_conversations:
                if participant in obj.participants.all() and obj.participants.all().count() == 2:
                    conversation = obj
                    room_messages = conversation.message_set.all()
                    return redirect('messages', conversation.id)
                
            conversation, room_messages = create_conversation(request, pk)                        
            return redirect('messages', conversation.id)
        except:
            try:
                conversation = Conversation.objects.get(id=pk)
                room_messages = conversation.message_set.all() 
            except:
                conversation, room_messages = create_conversation(request, pk)  ###   
                return redirect('messages', conversation.id)
        
    try:
        conversation_name = create_conversation_name(conversation)
    except:
        conversation_name = None

    context = {
        'following': following,
        'followers': followers,
        'conversations': conversations,
        'room_messages': room_messages,
        'conversation': conversation,
        'participants': participants,
        'conversation_name': conversation_name,
        # 'avatar': avatar,
    }
    return render(request, 'chat/messages.html', context)

@login_required(login_url="login")
def add_to_conversation(request, pk):
    conversation = Conversation.objects.get(id=pk)
    profiles = Profile.objects.all()
    conversation_profiles = conversation.participants.all()
    excludes = [request.user.profile.id]
    for participant in conversation_profiles:
        excludes.append(participant.id)  
    profiles = profiles.exclude(id__in=excludes)
    profiles, search = profile_search(request, profiles)   
    custom_range, profiles = paginate_profiles(request, profiles, 10)
    page = ''

    if request.method == 'POST':
        person_id = request.POST.get('person_id') 
        person = Profile.objects.get(id=person_id)
        conversation.participants.add(person)
        conversation.save()
        return redirect('messages', conversation.id)

    context = {
        'profiles': profiles,
        'page': page,
        'custom_range': custom_range,
        'search': search,
    }

    return render(request, 'chat/add_to_conversation.html', context)

@login_required(login_url="login")
def remove_from_conversation(request, pk):
    conversation = Conversation.objects.get(id=pk)
    profiles = conversation.participants.all()
    
    profiles, search = profile_search(request, profiles)
    custom_range, profiles = paginate_profiles(request, profiles, 10)
    page = ''


    if request.method == 'POST':
        person_id = request.POST.get('person_id') 
        person = Profile.objects.get(id=person_id)
        conversation.participants.remove(person)
        conversation.save()
        return redirect('messages', conversation.id)

    #variable to choose template functionality
    choose = 'remove'

    context = {
        'profiles': profiles,
        'page': page,
        'custom_range': custom_range,
        'search': search,
        'choose': choose,
    }

    return render(request, 'chat/add_to_conversation.html', context)

def participants(request, pk):
    conversation = Conversation.objects.get(id=pk)
    profiles = conversation.participants.all()

    
    profiles, search = profile_search(request, profiles)
    custom_range, profiles = paginate_profiles(request, profiles, 10)
    page = ''

    choose = 'participants'

    context = {
        'profiles': profiles,
        'page': page,
        'custom_range': custom_range,
        'search': search,
        'choose': choose,
    }

    return render(request, 'users/profiles.html', context)

# @login_required(login_url="login")
# def jam_request(request, pk):
