# Messaging App

This Django project implements a basic messaging API using Django REST Framework.

## Accomplishments

This project was built by completing the following tasks:

1.  **Configuration:**
    *   Abstracted sensitive settings (e.g., `SECRET_KEY`, `DATABASES`) into a `.env` file using `django-environ`.
    *   Configured Django REST Framework with default authentication and permission classes.

2.  **Data Modeling:**
    *   Designed and implemented custom models for `User`, `Conversation`, and `Message` in `chats/models.py`.
    *   Set up a custom user model (`AUTH_USER_MODEL`).

3.  **API Serialization:**
    *   Created serializers for the `User`, `Conversation`, and `Message` models in `chats/serializers.py`.
    *   Implemented nested serialization to include participants and messages within conversation data.

4.  **API Views & Endpoints:**
    *   Implemented `ConversationViewSet` and `MessageViewSet` in `chats/views.py` to handle API logic.
    *   Customized `perform_create` methods to automatically manage participants and senders.

5.  **URL Routing:**
    *   Configured URL patterns in `chats/urls.py` using `DefaultRouter` to automatically generate routes for the viewsets.
    *   Included the app's API routes under the `/api/` path in the main `messaging_app/urls.py`.

All code follows pycodestyle standards and includes docstrings for clarity.
