from django.urls import path
from . import views

urlpatterns = [
    path('jam-request/<uuid:pk>/', views.jam_request, name='jam-request')
]