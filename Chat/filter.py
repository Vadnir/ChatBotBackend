from django_filters import rest_framework as filters
import django_filters
from .models import Chat, ChatMessage


class ChatFilter(filters.FilterSet):

    class Meta:
        model = Chat
        fields = {
            'user__username': ['contains', 'exact'],
            'bot__id': ['contains', 'exact'],
        }


class ChatMessageFilter(filters.FilterSet):

    class Meta:
        model = ChatMessage
        fields = {
            'chat__id': ['exact'],
        }