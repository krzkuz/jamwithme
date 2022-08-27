from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('settings/', views.user_settings, name='settings'),
    path('skill/', views.user_skill, name='skill'),
    path('follow/<str:pk>', views.follow, name='follow'),
    path('unfollow/<str:pk>', views.unfollow, name='unfollow'),
    path('followers/<str:pk>', views.followers, name='followers'),
    path('messages/<str:pk>', views.users_messages, name='messages'),
    # path('message/<str:pk>', views.message, name='message'),
    path('send-message/<str:pk>', views.send_message, name='send_message'),
]