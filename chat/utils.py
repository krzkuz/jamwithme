from .models import Conversation
from users.models import Profile

def create_conversation(request, pk):
    participant = Profile.objects.get(id=pk)
    profile = Profile.objects.get(id=request.user.profile.id)
    # get all participant conversations
    conversations = participant.conversation_set.all()
    for obj in conversations:
        if profile in obj.participants.all():
            conversation = obj
    try:
        conversation
        room_messages = conversation.message_set.all()
    except:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user.profile, participant)
        conversation.save()
        # conversation name for database and chat functionality    
        conversation.name = str(conversation.id).replace('-', '')
        for participant in conversation.participants.all():
            conversation.name += str(participant.first_name)
        conversation.save()
        room_messages = None
    print(conversation)
    
    return conversation, room_messages

# conversation name to display
def create_conversation_name(conversation):
    conversation_name = ''
    i = 1
    for participant in conversation.participants.all():
        conversation_name += str(participant.first_name)
        if i < conversation.participants.all().count():
            conversation_name += ', '
            i += 1
    return conversation_name

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