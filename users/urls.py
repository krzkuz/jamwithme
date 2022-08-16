from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('account/', views.user_account, name='account'),
]