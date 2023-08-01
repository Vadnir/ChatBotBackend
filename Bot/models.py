import uuid
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    tag = models.CharField(max_length=64, default="")


# Create your models here.
class Bot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=40, verbose_name='bot name')
    description = models.TextField(max_length=500, verbose_name='bot description')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'
        ordering = ['-created']

    def __str__(self):
        return self.name


class BotCategories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'BotCategories'
        verbose_name_plural = 'BotsCategories'
        ordering = ['-bot']


class BotCharacter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    temperature = models.FloatField(default=0.5)
    max_tokens = models.IntegerField(default=500)
    presence_penalty = models.FloatField(default=0.5)
    frequency_penalty = models.FloatField(default=0.5)
    stream = models.BooleanField(default=False)
    first_message = models.CharField(max_length=512, default="")
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)


class BotMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    content = models.CharField(max_length=1024, default="")
    rol = models.BooleanField(default=True, null=False)
    bot_character = models.ForeignKey(BotCharacter, on_delete=models.CASCADE)