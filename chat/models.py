from django.db import models
from users.models import Profile
import uuid

class Conversation(models.Model):
    participants = models.ManyToManyField(Profile, blank=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    # field to hide conversation from specified user if he deletes conversation
    not_show_for = models.ManyToManyField(Profile, blank=True, related_name='not_show_conversation')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=False)
    # field to hide message from specified user if he deletes conversation
    not_show_for = models.ManyToManyField(Profile, blank=True, related_name='not_show_message')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.body[:30]
    
    class Meta:
        ordering = ['created']


