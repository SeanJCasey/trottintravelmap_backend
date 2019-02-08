from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from places.models import Place

from .serializers import PlaceSerializer, UserSerializer

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
