# from asyncio.windows_events import NULL
# import email
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_youtube = models.CharField(max_length=300, null=True, blank=True)
    social_facebook = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def image_url(self):
        try: 
            url = self.profile_image.url
        except:
            url = ''
        return url    
    
    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class Follow(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=False)
    follower = models.ManyToManyField(Profile, blank=True, related_name='follower')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)


class Instrument(models.Model):
    player = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    level_choices = [
        ('Novice', 'Novice'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]
    level = models.CharField(max_length=20, choices=level_choices)

    def __str__(self):
        return self.name