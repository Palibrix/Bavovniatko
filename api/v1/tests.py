from rest_framework.test import APITestCase
from mixer.backend.django import mixer

from components.models import Stack, FlightController, SpeedController, Antenna


# Not implemented yet. Will be creating users here
class BaseAPITest(APITestCase):
    mixer.register(Antenna,
                   description='TestAntenna',
                   bandwidth_min=1.0,
                   bandwidth_max=20.0,
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

