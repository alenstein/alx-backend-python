"""
Main URL configuration for the messaging_app project.

This module routes URLs to the appropriate apps and views.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from messaging_app.chats.auth import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
