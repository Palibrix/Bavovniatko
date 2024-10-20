from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.components.views import AntennaAPIViewSet

app_name = 'api-v1-components'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaAPIViewSet, basename="antenna")

urlpatterns = [

] + router.urls
