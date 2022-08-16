from django.db import models
from users.models import Profile
import uuid

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    #picture
    #record
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-created']


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.body[:30]+'...'


class Rate(models.Model):
    rate_choices = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.CharField(max_length=200, choices=rate_choices)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.rate