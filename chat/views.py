from django.shortcuts import render
from .models import Message, Conversation
from users.models import Profile, Follow
from .utils import create_conversation, create_conversation_name

def users_messages(request, room_name):
    # profiles = Profile.objects.all()
    profile = Profile.objects.get(user=request.user)
    follow = Follow.objects.get(user=profile)
    following = profile.follower.all()
    followers = follow.follower.all()
    user = Profile.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(participants__in=user).order_by('updated')
    participants = user
    all_messages = Message.objects.none()
    # variable to choose template 'profiles' funcionality
    page = 'message'
    # getting queryset of all conversations participants and messages
    for conversation in conversations:
        participants = participants | conversation.participants.all()
        all_messages = all_messages | conversation.message_set.all()
    if room_name == 'None':
        try:
            last_message = all_messages.last()
            conversation = last_message.conversation
            room_messages = conversation.message_set.all()
        except:
            conversation = None
            room_messages = None
    else:
        conversation, room_messages = create_conversation(request, profile, room_name)        

    try:
        conversation_name = create_conversation_name(request, conversation)
    except:
        conversation_name = None

    
    # New message 
    # if conversation:    
    #     form = send_message(request, conversation)
    #     #return redirect('messages', pk)
    # else:
    #     form = None

    # if not room_messages:
    #     try:
    #         conversation.delete()
    #     except:
    #         pass
    # function to display avatar only on last written message by the user
    # avatar = conversation_avatar(request, conversation)

    context = {
        'following': following,
        'followers': followers,
        'conversations': conversations,
        'room_messages': room_messages,
        'conversation': conversation,
        'participants': participants,
        'conversation_name': conversation_name,
        'page': page,
        # 'profiles': profiles,
        # 'avatar': avatar,
    }
    return render(request, 'chat/messages.html', context)

