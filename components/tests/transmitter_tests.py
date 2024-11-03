from unittest import TestCase

from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import Antenna, Transmitter


class TestTransmitterModel(TestCase):

    def setUp(self):
        mixer.register(Transmitter,
                       description='TestTransmitter',
                       output_voltage=1.0,
                       channels_quantity=2.0
                       )

    def test_voltage_incorrect(self):
        with self.assertRaises(ValidationError):
            mixer.blend(Transmitter,
                        input_voltage_min=2.0,
                        input_voltage_max=1.0,)
