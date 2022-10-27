from django import template
from notification.models import Notification

register = template.Library()

# @register.inclusion_tag('')