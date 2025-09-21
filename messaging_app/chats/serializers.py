"""
Serializers for the chats app.

This module defines serializers for the User, Message, and Conversation
models, which are used to convert model instances into JSON representations
and vice versa. These serializers are essential for building the API
endpoints that expose the app's data.
"""
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles the conversion of User model instances
    to and from JSON format, exposing key user attributes.
    """
    class Meta:
        """
        Meta class for UserSerializer.

        Defines the model and fields to be serialized.
        """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    This serializer converts Message model instances into JSON,
    including the sender, message body, and timestamp.
    """
    class Meta:
        """
        Meta class for MessageSerializer.

        Specifies the model and the fields to include in the
        serialized output.
        """
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.

    This serializer provides a detailed view of a conversation, including
    nested representations of its participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for ConversationSerializer.

        Links the serializer to the Conversation model and specifies
        the fields to be included, along with nested serializers.
        """
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
