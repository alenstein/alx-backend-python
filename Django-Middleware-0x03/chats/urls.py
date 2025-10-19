"""
URL configurations for the chats app.

This module defines the URL patterns for the chats app, mapping the
Conversation and Message viewsets to their respective API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserCreateAPIView

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('', include(router.urls)),
]
