from .forms import MessageForm
from .models import Conversation, Message
from users.models import Profile
from django.shortcuts import render, redirect

def send_message(request, conversation): 
    form = MessageForm()     
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.conversation = conversation
            message.save()  
    form = MessageForm()               
        #return redirect('messages', pk)
    return form

def create_conversation(request, profile, pk):
    participant = Profile.objects.get(id=pk)
    conversation, created = Conversation.objects.get_or_create(id=pk)
    # if created:
    #     conversation.id = uuid.uuid4
    conversation.participants.add(profile, participant)
    room_messages = conversation.message_set.all()
    conversation.name = ''
    i = 1
    for participant in conversation.participants.all():
        conversation.name += str(participant.first_name)
        if i < conversation.participants.all().count():
            conversation.name += ', '
            i += 1
    conversation.save()
    return conversation, room_messages

# def conversation_avatar(request, conversation):
#     # room_messages = conversation.message_set.all()
#     last_messages = conversation.message_set.all().order_by('-created')[0:2]
#     if last_messages[0].sender == last_messages[1].sender:
#         return False
#     else:
#         return True
    # for message in room_messages:
    #     if message[-1].sender == message 
    #         return True
    #     else:
    #         return False