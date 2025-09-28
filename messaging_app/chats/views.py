"""
Views for the chats app.

This module defines the viewsets for the Conversation and Message models,
which handle the API logic for listing, creating, and managing conversations
and messages. These viewsets are the core of the app's API functionality.
"""
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserCreateSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing conversation instances.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        """
        Create a new conversation and add the current user as a participant.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing message instances.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        This view should return a list of all messages in conversations
        the user is part of.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        """
        Create a new message and set the current user as the sender.
        Users can only create messages in conversations they are a part of.
        """
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only create messages in conversations you are a part of.")
        serializer.save(sender=self.request.user)
