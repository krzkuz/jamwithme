from django.db import models
from users.models import Profile
import uuid

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=False)
    body = models.TextField(null=True, blank=False)
    picture = models.ImageField(null=True, blank=True, upload_to='posts/')
    record = models.FileField(null=True, blank=True, upload_to='records/')
    tags = models.ManyToManyField('Tag', blank=False)
    likes = models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField(Profile, blank=True, related_name='post_dislikes')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    @property
    def image_url(self):
        try: 
            url = self.picture.url
        except:
            url = ''
        return url

    @property
    def video_url(self):
        try: 
            url = self.record.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.subject


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=False)
    likes = models.ManyToManyField(Profile, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(Profile, blank=True, related_name='comment_dislikes')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[:30]


