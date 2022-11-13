from django import template
from notification.models import Notification
from users.models import Profile

register = template.Library()

@register.inclusion_tag('notification/notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    profile = Profile.objects.filter(user=request_user)
    notifications = Notification.objects.filter(to_users__in=profile).order_by('-created')
    unseen = notifications.exclude(seen=True)
    return {
        'notifications': notifications,
        'unseen': unseen,
    }