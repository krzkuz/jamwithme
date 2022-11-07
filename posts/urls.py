from django.urls import path
from . import views


urlpatterns = [
    path('<uuid:pk>/', views.post, name='post'),
    path('', views.posts, name='posts'),
    path('create-post', views.create_post, name='create-post'),
    path('update-post/<uuid:pk>', views.update_post, name='update-post'),
    path('delete-post/<uuid:pk>', views.delete_post, name='delete-post'),
    path('like-post/', views.like_post, name='like-post'), 
    path('dislike-post/', views.dislike_post, name='dislike-post'), 
    path('like-comment/<uuid:pk>', views.like_comment, name='like-comment'),
    path('dislike-comment/<uuid:pk>', views.dislike_comment, name='dislike-comment'),
    path('create-comment/', views.create_comment, name='create-comment'),
    path('delete-comment', views.delete_comment, name='delete-comment'),
    # path('django-messages/', views.django_messages, name='django-messages'),
    
]