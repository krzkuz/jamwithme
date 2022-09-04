from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.users_messages, name='messages'),
]