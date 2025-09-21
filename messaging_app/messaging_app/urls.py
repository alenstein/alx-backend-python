"""
Main URL configuration for the messaging_app project.

This module routes URLs to the appropriate apps and views.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
]
