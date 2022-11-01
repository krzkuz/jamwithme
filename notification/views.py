from django.shortcuts import redirect
from notification.models import JamRequest, Notification
from users.models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def jam_request(request, pk):
    JamRequest.objects.create(
        sender = request.user.profile,
        recipient = Profile.objects.get(id=pk)
    )
    return redirect(request.META.get('HTTP_REFERER'))

def notification_seen(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.seen = True
    notification.save()
    return redirect(notification.link)
