from django.urls import path
from rest_framework.authtoken import views
from .views import UserListView, UserCreateView
"""
urls for the user api
"""
urlpatterns = [
    path('list', UserListView.as_view()),
    path('create', UserCreateView.as_view()),
    path('auth/', views.obtain_auth_token),
]
