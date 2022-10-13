from django.shortcuts import render, redirect
from .models import Message, Conversation
from users.models import Profile, Follow
from .utils import create_conversation, create_conversation_name
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def users_messages(request, pk):
    profile = Profile.objects.get(user=request.user)
    follow = Follow.objects.get(user=profile)
    following = profile.follower.all()
    followers = follow.follower.all()
    user = Profile.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(participants__in=user).order_by('updated')
    participants = user
    all_messages = Message.objects.none()

    # getting queryset of all conversations participants and messages
    for conversation in conversations:
        participants = participants | conversation.participants.all()
        all_messages = all_messages | conversation.message_set.all()
    if pk == 'None':
        try:
            last_message = all_messages.last()
            conversation = last_message.conversation
            room_messages = conversation.message_set.all()
        except:
            conversation = None
            room_messages = None
    elif Conversation.objects.filter(id=pk).exists():
        conversation = Conversation.objects.get(id=pk)
        room_messages = conversation.message_set.all() 
    else:
        conversation, room_messages = create_conversation(request, pk)  ###   
        return redirect('messages', conversation.id)       

    try:
        conversation_name = create_conversation_name(conversation)
    except:
        conversation_name = None

    # try:
    #         conversation, room_messages = create_conversation(request, profile, pk)  ###   
    #     except:
    #         conversation = Conversation.objects.get(id=pk)
    #         room_messages = conversation.message_set.all() 

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
        # 'avatar': avatar,
    }
    return render(request, 'chat/messages.html', context)

