from django.urls import path
from . import views

urlpatterns = [
    path('jam-request/<uuid:pk>/', views.jam_request, name='jam-request'),
    path('notification-seen/<uuid:pk>', views.notification_seen, name="notification-seen"),
    path('get-new-notifications', views.get_new_notifications, name='get-new-notifications'),
    path('delete-notification', views.delete_notification, name='delete-notification')
    # path('notifications/', views.notifications, name='notifications'),
]