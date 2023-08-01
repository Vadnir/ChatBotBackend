from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters import rest_framework as filters
from .serializer import BotSerializer, BotCategorySerializer
from .models import Bot, BotCategories, Category, BotCharacter, BotMessages
from .pagination import StandardResultsSetPagination
from .filter import BotFilter
from PIL import Image


# Create your views here.
class BotListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = BotCategories.objects.all()
    serializer_class = BotCategorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filterset_class = BotFilter


class BotView(generics.CreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    def create(self, request, *args, **kwargs):

        data = request.data
        try:
            new_bot = Bot.objects.create(
                name=data['name'],
                description=data['description'],
                author=request.user,
                active=True
            )
            new_bot.save()
        except Exception as e:
            last_error = e
            return Response(status=401)

        if "categories" in data.keys():

            categories = list(map(lambda x: x.lower(), (data['categories'].split(";"))))
            cats = Category.objects.filter(tag__in=categories)

            for i in cats:
                BotCategories.objects.create(
                    tag=i,
                    bot=new_bot
                ).save()

        if "character" in data.keys():

            new_bot_character = BotCharacter.objects.create(
                bot=new_bot, **data['character']['params']
            )
            new_bot_character.save()

            for i in data['character']['messages']:
                BotMessages.objects.create(
                    bot_character=new_bot_character,
                    **i
                ).save()

        return Response(status=201)

    def destroy(self, request, *args, **kwargs):

        data = request.data

        bot = Bot.objects.filter(id=data['bot_id'])
        if len(bot) < 1:
            return Response(status=401)
        bot = bot[0]

        if bot.author != request.user:
            return Response(status=404)

        bot.delete()


class BotImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (AllowAny,)

    def post(self, request, format=None):  # request.body es la imagen
        bot_id = request.data['id']
        image = request.data['image']

        bot = Bot.objects.filter(id=bot_id)
        if len(bot) < 1:
            return Response(status=401)
        bot = bot[0]

        if bot.id != bot_id:
            return Response(status=404)

        img = Image.open(image)
        img.save(f"media/bot_images/{bot_id}", 'jpeg')

        return Response(status=201)


class BotAdminView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)