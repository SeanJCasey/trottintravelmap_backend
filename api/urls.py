from django.urls import path, include

from rest_framework import routers

from . import views


app_name = 'api'

router = routers.DefaultRouter(trailing_slash=False)

router.register('places', views.PlaceViewSet, base_name='place')
router.register('placemaps', views.PlaceMapViewSet, base_name='placemap')
router.register('users', views.UserViewSet, base_name='user')

urlpatterns = router.urls
