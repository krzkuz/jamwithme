from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.users_messages, name='messages'),
    path('add-to-conversation/<uuid:pk>/', views.add_to_conversation, name='add-to-conversation'),
    path('remove-from-conversation/<uuid:pk>/', views.remove_from_conversation, name='remove-from-conversation'),
    path('participants/<uuid:pk>/', views.participants, name='participants'),
    path('delete-conversation/<uuid:pk>/', views.delete_conversation, name='delete-conversation')
]