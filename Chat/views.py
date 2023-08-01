from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Bot.models import Bot, BotCharacter, BotMessages
from .CharResponse.CharResponse import CharResponse
from .Encrypt.Encrypter import Encrypter
from .filter import ChatFilter, ChatMessageFilter
from .models import Chat, ChatMessage
from .pagination import StandardResultsSetPagination
from .serializer import ChatSerializer, ChatMessageSerializer


# Create your views here.
class ChatListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatMessageSerializer
    queryset = Chat.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filterset_class = ChatMessageFilter


class ChatMessageListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filterset_class = ChatFilter


class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data

        bot = Bot.objects.filter(id=data['bot_id'])
        if len(bot) < 1:
            return Response(status=401)
        bot = bot[0]

        bot_character = BotCharacter.objects.filter(bot=bot)
        if not bot_character:
            return Response(status=401)
        bot_character = bot_character[0]

        new_chat = Chat.objects.create(
            user=request.user,
            bot=bot
        )
        new_chat.save()

        ChatMessage.objects.create(
            rol=False, content=bot_character.first_message,
            chat=new_chat
        ).save()

        return Response(status=201)


class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        data = request.data

        chat = Chat.objects.filter(id=data['chat_id'])
        if not chat:
            return Response(status=401)
        chat = chat[0]

        if data['type'] == "prompt":

            token = Token.objects.filter(key=request.auth)[0]

            e = Encrypter(
                token.key
            )

            ChatMessage.objects.create(
                rol=True, content=data['content'],
                chat=chat
            ).save()

            del e

            return Response(status=201)

        else:

            bot_character = BotCharacter.objects.filter(bot=chat.bot)
            if not bot_character:
                return Response(status=401)
            bot_character = bot_character[0]

            bot_messages = BotMessages.objects.filter(bot_character=bot_character)
            if not bot_messages:
                return Response(status=401)
            bot_messages = bot_messages[0]

            chat_messages = ChatMessage.objects.filter(chat=chat)
            if not bot_messages:
                return Response(status=401)
            chat_messages = chat_messages[0]

            chat_response = CharResponse(
                method="", bot=chat.bot,
                bot_character=bot_character, bot_messages=bot_messages,
                chat_messages=chat_messages
            )

            return Response(
                {
                    "content": chat_response.get_response()
                }
            )