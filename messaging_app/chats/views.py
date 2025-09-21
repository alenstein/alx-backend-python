"""
Views for the chats app.

This module defines the viewsets for the Conversation and Message models,
which handle the API logic for listing, creating, and managing conversations
and messages. These viewsets are the core of the app's API functionality.
"""
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing conversation instances.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def perform_create(self, serializer):
        """Create a new conversation and add the current user as a participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing message instances.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """Create a new message and set the current user as the sender."""
        serializer.save(sender=self.request.user)
