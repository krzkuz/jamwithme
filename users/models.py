from asyncio.windows_events import NULL
import email
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_youtube = models.CharField(max_length=300, null=True, blank=True)
    social_facebook = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=False)
    follower = models.ManyToManyField(Profile, blank=True, related_name='follower')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)



class Conversation(models.Model):
    participants = models.ManyToManyField(Profile, blank=True)
    name = models.CharField(max_length=250, blank=True, null=True, default='noname')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # @property
    # def name(self):
    #     if self.name == 'noname':
    #         new_name = ''
    #         query_set = self.participants.all()
    #         for participant in query_set:
    #             new_name = new_name + participant.first_name + ' ' + participant.last_name + ','           
    #     return new_name
        # @property
        # def change_name(self):
        # if self.name == 'noname':
        #     new_name = ''
        #     query_set = self.participants.all()
        #     for participant in query_set:
        #         new_name = new_name + participant.first_name + ' ' + participant.last_name + ','           
        # return new_name
    # @property
    # def name(self):
    #     if self.name == 'noname':
    #         self.name = ''
    #         query_set = self.participants.all()
    #         for participant in query_set:
    #             self.name = self.name + participant.first_name + ' ' + participant.last_name + ','           
    #     return self.name

    

        # try:
        #     conversation_name = 'exp'
        # except:
        #     conversation_name != 'noname'
        # return conversation_name
        # if name == 'NULL':
        #     #name = self.participants.all()
        #     name = '++++++++++++++++++++'
        # else:
        #     name = self.name+'qwe'

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    # recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.body[:30]
    
    class Meta:
        ordering = ['created']


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