from .models import Message, Conversation
from django.db.models.signals import post_save, post_delete, pre_save
import datetime

def update_conversation(sender, instance, created, **kwargs):
    if created:
        message = instance
        conversation = message.conversation
        conversation.updated = datetime.datetime.now()
        conversation.save()

post_save.connect(update_conversation, sender=Message)