from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from mixer.backend.django import mixer

from components.models import Antenna, AntennaDetail


class TestAntennaModel(TestCase):

    def setUp(self):
        mixer.register(Antenna,
                       description='TestAntenna',
                       )
        self.antenna = mixer.blend(Antenna,
                                   bandwidth_min=1.0,
                                   bandwidth_max=2.0,
                                   center_frequency=1.5)

    def test_frequency_incorrect(self):
        with self.assertRaises(ValidationError):
            mixer.blend(Antenna,
                        bandwidth_min=2.0,
                        bandwidth_max=1.0,
                        center_frequency=1.5)

    def test_frequency_correct(self):
        self.assertEqual(self.antenna.center_frequency, 1.5)

    def test_delete_detail(self):
        mixer.cycle(2).blend(AntennaDetail, antenna=self.antenna)
        self.assertEqual(self.antenna.details.count(), 2)

        detail_to_delete = self.antenna.details.first()
        detail_to_delete.delete()

        self.assertEqual(self.antenna.details.count(), 1)

    def test_delete_only_detail(self):
        antenna_detail = mixer.blend(AntennaDetail, antenna=self.antenna)
        self.assertEqual(self.antenna.details.count(), 1)

        with self.assertRaises(ProtectedError):
            antenna_detail.delete()
