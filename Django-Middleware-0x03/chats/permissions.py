from rest_framework import permissions

class IsParticipantOfConversation(permissions.IsAuthenticated):
    """
    Custom permission to only allow authenticated participants of a conversation to access it or its messages.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation or the message's conversation.
        if hasattr(obj, 'participants'): # Conversation object
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'): # Message object
            return request.user in obj.conversation.participants.all()
        return False
