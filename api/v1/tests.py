from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from builds.models import Drone
from components.models import Stack, FlightController, SpeedController, Antenna, Transmitter, Camera, Frame
from suggestions.models import AntennaSuggestion, CameraSuggestion, FrameSuggestion
from users.tests import BaseUserTest


class BaseAPITest(APITestCase, BaseUserTest):
    mixer.register(Antenna,
                   description='TestAntenna',
                   bandwidth_min=1.0,
                   bandwidth_max=20.0,
                   center_frequency=15
                   )

    mixer.register(AntennaSuggestion,
                   description='TestAntennaSuggestion',
                   bandwidth_min=1.0,
                   bandwidth_max=20.0,
                   center_frequency=15
                   )

    mixer.register(Camera,
                   description='TestCamera',
                   voltage_min=2,
                   voltage_max=10,
                   fov=180)


    mixer.register(CameraSuggestion,
                   description='TestCamera',
                   voltage_min=2,
                   voltage_max=10,
                   fov=180)

    mixer.register(Drone,
                   description='TestDrone',
                   )

    mixer.register(Frame,
                   description='TestFrame',
                   )

    mixer.register(FrameSuggestion,
                   description='TestFrameSuggestion',
                   )

    mixer.register(Stack,
                   description='TestStack',
                   )

    mixer.register(FlightController,
                   description='TestFlightController',
                   weight=15,
                   )

    mixer.register(SpeedController,
                   description='TestSpeedController',
                   weight=15,
                   cont_current=15,
                   burst_current=20,
                   )

    mixer.register(Transmitter,
                   description='TestTransmitter',
                   output_voltage=1.0,
                   channels_quantity=2,
                   input_voltage_min=1.0,
                   input_voltage_max=2.0,
                   )


    def create_and_login(self, username="test", email='test@mail.com', password='test_password', is_super=False):
        user = self.create(username=username, email=email, password=password, is_super=is_super)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)