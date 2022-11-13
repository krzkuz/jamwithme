from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.get_routes),
    path('posts/', views.get_posts),
    path('posts/<uuid:pk>/', views.get_post),
    path('posts/<uuid:pk>/vote/', views.post_vote),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
