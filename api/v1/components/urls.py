from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.components.views import (AntennaAPIViewSet, CameraAPIViewSet, FrameAPIViewSet, MotorAPIViewSet,
                                     PropellerAPIViewSet)

app_name = 'api-v1-components'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaAPIViewSet, basename="antenna")
router.register(r'cameras', CameraAPIViewSet, basename="camera")
router.register(r'frames', FrameAPIViewSet, basename="frame")
router.register(r'motors', MotorAPIViewSet, basename="motor")
router.register(r'propellers', PropellerAPIViewSet, basename="propeller")

urlpatterns = [

] + router.urls
