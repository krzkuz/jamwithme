from django.db.models.signals import post_save

from .models import JamRequest, Notification

def jam_request_notification(sender, instance, created, **kwargs):
    if created:
        jam_request = instance
        Notification.objects.create(
            type = 3,
            from_user = jam_request.sender,
            to_user = jam_request.recipient,            
        )

post_save.connect(jam_request_notification, sender=JamRequest)

# def post_notification(sender, instance, created, **kwargs):
#     if created:
#         jam_request = instance
#         Notification.objects.create(
#             type = 3,
#             from_user = jam_request.sender,
#             to_user = jam_request.recipient,            
#         )

# post_save.connect(post_notification, sender=JamRequest)