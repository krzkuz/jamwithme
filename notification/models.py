from django.db import models
from users.models import Profile
from posts.models import Post, Comment
from chat.models import Message
import uuid

class JamRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name = 'recipient')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return 'Jam request from ' + self.sender.first_name + ' ' + self.sender.last_name 


class Notification(models.Model):
    # type 1-like, 2-comment, 3-jamrequest, 4-message?
    type = models.IntegerField()
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='to_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
