import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.CharFilter(field_name='conversation__id')
    sender = django_filters.CharFilter(field_name='sender__username')
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']
