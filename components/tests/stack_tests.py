from unittest import TestCase

from mixer.backend.django import mixer

from components.models import Stack, FlightController, SpeedController


class TestStackModel(TestCase):

    def setUp(self):
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

        self.flight_controller1 = mixer.blend(FlightController,
                                              manufacturer='Manufacturer1',
                                              )
        self.speed_controller1 = mixer.blend(SpeedController,
                                             manufacturer='Manufacturer1',
                                             )

        self.speed_controller2 = mixer.blend(SpeedController,
                                             manufacturer='Manufacturer2',
                                             )

        self.stack = mixer.blend(Stack, flight_controller=self.flight_controller1,
                                 speed_controller=self.speed_controller1)

    def test_is_in_stack(self):
        self.assertTrue(self.flight_controller1.is_in_stack())
        self.assertFalse(self.speed_controller2.is_in_stack())
