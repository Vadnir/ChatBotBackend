from django.urls import path, include
from .views import BotView, BotImageUpload, BotListView
"""
urls for the bot api
"""

urlpatterns = [
    path('', BotView.as_view()),
    path('list', BotListView.as_view()),
    path('image', BotImageUpload.as_view()),
]
