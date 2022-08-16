from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.post, name='post'),
    path('', views.posts, name='posts')
]