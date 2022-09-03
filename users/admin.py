from django.contrib import admin
from .models import Profile, Message, Instrument, Follow, Conversation
# Register your models here.
    
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Instrument)
admin.site.register(Follow)
admin.site.register(Conversation)

