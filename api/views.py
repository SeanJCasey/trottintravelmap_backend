from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from places.models import Place, PlaceMap

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
    permission_classes = (AllowAny,)
    queryset = PlaceMap.objects.filter(user__pk=1)
    # queryset = PlaceMap.objects.filter(user=self.request.user)
