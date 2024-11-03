from rest_framework.test import APITestCase
from mixer.backend.django import mixer

from builds.models import Drone
from components.models import Stack, FlightController, SpeedController, Antenna, Transmitter


class BaseAPITest(APITestCase):
    mixer.register(Antenna,
                   description='TestAntenna',
                   bandwidth_min=1.0,
                   bandwidth_max=20.0,
                   center_frequency=15
                   )

    mixer.register(Drone,
                   description='TestDrone',
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
