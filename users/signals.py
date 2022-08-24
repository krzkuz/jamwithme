import email
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile

def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user
        )

post_save.connect(create_profile, sender=User)

def update_user(sender, instance, created, **kwargs):
    if created == False:
        user = instance.user
        if user.first_name:
            user.first_name = instance.first_name
        if user.last_name:
            user.last_name = instance.last_name
        if user.email:
            user.email = instance.email
        user.save()

post_save.connect(update_user, sender=Profile)

def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_delete.connect(delete_user, sender=Profile)