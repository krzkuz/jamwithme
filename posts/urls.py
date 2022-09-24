from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.post, name='post'),
    path('', views.posts, name='posts'),
    path('create-post', views.create_post, name='create-post'),
    path('update-post/<str:pk>', views.update_post, name='update-post'),
    path('delete-post/<str:pk>', views.delete_post, name='delete-post'),
    path('like-post/<str:pk>', views.like_post, name='like-post'),
    path('dislike-post/<str:pk>', views.dislike_post, name='dislike-post'),
    path('like-comment/<str:pk>', views.like_comment, name='like-comment'),
    path('dislike-comment/<str:pk>', views.dislike_comment, name='dislike-comment'),
]