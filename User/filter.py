import django_filters

from django.contrib.auth.models import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = {
            'username': ['contains', 'exact'],
        }
        exclude = ['password', 'email']