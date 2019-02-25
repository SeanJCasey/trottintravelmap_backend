from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from places.models import Place, PlaceMap

from .permissions import IsOwnerOrReadOnly
from .serializers import PlaceSerializer, PlaceMapSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        # NOTE: can remove read logic
        if not self.request.user.is_authenticated:
            return []

        return User.objects.filter(email=self.request.user.email)


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = (AllowAny,)
    queryset = Place.objects.all()


class PlaceMapViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceMapSerializer
    queryset = PlaceMap.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]
