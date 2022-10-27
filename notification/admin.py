from django.contrib import admin
from .models import Notification, JamRequest

admin.site.register(Notification)
admin.site.register(JamRequest)