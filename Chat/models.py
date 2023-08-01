import datetime

from django.db import models
from django.contrib.auth.models import User
import uuid
from Bot.models import Bot


# Create your models here.
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-bot']


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rol = models.BooleanField(default=True, null=False)
    content = models.TextField(max_length=4096, null=True, default="")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created']
