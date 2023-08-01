import django_filters

from .models import Bot, BotCategories
from django_filters import rest_framework as filters


class BotFilter(filters.FilterSet):

    category = django_filters.MultipleChoiceFilter(default="")

    class Meta:
        model = BotCategories
        fields = {
            'category__tag': ['contains', 'exact'],
        }