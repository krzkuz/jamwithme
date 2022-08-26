from django.contrib import admin
from .models import Profile, Message, Instrument, Follow
# Register your models here.

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Instrument)
admin.site.register(Follow)