from .models import Conversation
from users.models import Profile
from django.db.models import Q

def create_conversation(request, pk):
    participant = Profile.objects.get(id=pk)
    profile = Profile.objects.get(id=request.user.profile.id)
    conversation = Conversation.objects.create()
    conversation.participants.add(profile, participant)  
    conversation.name = str(conversation.id).replace('-', '')
    conversation.save()
    room_messages = None
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

def profile_search(request, all_profiles):
    search = request.GET.get('q')
    if search:
        search_list = str(search).split()
        profiles = Profile.objects.none()
        for word in search_list:
            profiles = profiles | all_profiles.distinct().filter(
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word)
            )
    else:
        search = ''
        profiles = all_profiles
    return profiles, search



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