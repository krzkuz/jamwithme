from django.shortcuts import redirect
from notification.models import JamRequest, Notification
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

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

def get_new_notifications(request):
    profile = Profile.objects.filter(user=request.user)
    notifications_query_set = Notification.objects.filter(to_users__in=profile).exclude(seen=True)
    notifications = [{
        'id': notification.id , 
        'name': notification.name,
        'image': notification.notification_image,
        'link': reverse('notification-seen', args=[notification.id]) 
    } for notification in notifications_query_set]

    return JsonResponse(notifications, safe=False)

@login_required(login_url="login")
def delete_notification(request):
    pk = request.POST.get('id')
    print(pk)
    notification = Notification.objects.get(id=pk)
    notification.delete()
    return HttpResponse("")