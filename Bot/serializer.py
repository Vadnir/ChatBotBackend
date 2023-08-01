from rest_framework import serializers
from .models import Bot, BotCategories


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'


class BotCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model: BotCategories
        fields = '__all__'