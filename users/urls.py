from django.urls import path
from . import views

urlpatterns = [
    path('profile/<uuid:pk>/', views.profile, name='profile'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('settings/', views.user_settings, name='settings'),
    path('skill/', views.user_skill, name='skill'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('follow/<uuid:pk>', views.follow, name='follow'),
    path('unfollow/<uuid:pk>', views.unfollow, name='unfollow'),
    path('followers/<uuid:pk>', views.followers, name='followers'),
    path('following/<uuid:pk>', views.following, name='following'),
    path('profiles/', views.profiles, name='profiles')
]
