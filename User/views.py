from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User, UserManager
from django_filters import rest_framework as filters
from .serializer import UserSerializer
from .pagination import StandardResultsSetPagination
from .filter import UserFilter

# Create your views here.


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filterset_class = UserFilter


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        data = request.data

        new_user = UserManager().create_user(
            username=data['username'], password=data['password'],
            email=data['email'],
        )
        new_user.save()
        print(new_user)
        return Response(status=201)