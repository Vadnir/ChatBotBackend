from django.urls import path
from .views import ChatListView, ChatCreateView

"""
urls for the user api
"""
urlpatterns = [
    path("list/", ChatListView.as_view()),
    path("create/", ChatCreateView.as_view())
]
