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
    # type 1-like/dislike(post, comment), 2-comment(post), 3-jamrequest, 4-follow
    type = models.IntegerField(null=True, blank=True)
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='from_user')
    to_users = models.ManyToManyField(Profile, related_name='to_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)#like comment 
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)#like 
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)#
    link = models.URLField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # @property
    # def url(self):
    class Meta:
        ordering = ['-created']
    @property
    def notification_image(self):
        return self.from_user.image_url

    @property
    def name(self):
        #post notification
        if self.post:
            if self.type == 1:
                name = str(self.from_user) + ' reacted to your post'
                return name
            else:
                name = str(self.from_user) + ' commented your post'
                return name
        #comment notification  
        elif self.comment:
            name = str(self.from_user) + ' reacted to your comment'
            return name
        elif self.message:
            name = 'New message from ' + str(self.from_user)
            return name
        elif self.type == 3:
            #jamrequest
            name = str(self.from_user) + ' sent you jam request'
            return name
        elif self.type == 4:
            #follow
            name = str(self.from_user) + ' is following you'
            return name
        else:
            name = 'Notification'
            return name