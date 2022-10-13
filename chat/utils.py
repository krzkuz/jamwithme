from .models import Conversation
from users.models import Profile
from django.db.models import Q

def create_conversation(request, pk):
    participant = Profile.objects.get(id=pk)
    try:
        conversation = Conversation.objects.filter(
            Q(participants__in=participant) &
            Q(participants__in=request.user.profile)
            )
    except:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user.profile, participant)
        room_messages = None

    # conversation name for database and chat functionality
    conversation.name = ''
    for participant in conversation.participants.all():
        conversation.name += str(participant.first_name)
    conversation.save()
    return conversation, room_messages

'''
participant = Profile.objects.get(id=pk)
    conversation, created = Conversation.objects.get_or_create(id=pk)
    # if created:
    #     conversation.id = uuid.uuid4
    conversation.participants.add(profile, participant)
    room_messages = conversation.message_set.all()

    # conversation name for database and chat funcionality
    conversation.name = ''
    for participant in conversation.participants.all():
        conversation.name += str(participant.first_name)
    conversation.save()
    conversation.save()
    return conversation, room_messages
'''
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