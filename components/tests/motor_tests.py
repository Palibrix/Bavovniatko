from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from mixer.backend.django import mixer

from components.models import Motor, MotorDetail, RatedVoltage


class TestMotorModel(TestCase):

    def setUp(self):
        mixer.register(Motor,
                       description='TestMotor',
                       stator_diameter='26',
                       stator_height='06',
                       )
        self.voltage = mixer.blend(RatedVoltage, min_cells=6, max_cells=2)
        mixer.register(MotorDetail,
                       weight=10,
                       peak_current=10,
                       idle_current=10,
                       resistance=10,
                       voltage=self.voltage,)
        self.motor = mixer.blend(Motor)



    def test_motor_delete_detail(self):
        mixer.cycle(2).blend(MotorDetail, motor=self.motor, voltage=self.voltage)
        self.assertEqual(self.motor.details.count(), 2)

        detail_to_delete = self.motor.details.first()
        detail_to_delete.delete()

        self.assertEqual(self.motor.details.count(), 1)

    def test_motor_delete_only_detail(self):
        motor_details = mixer.blend(MotorDetail, motor=self.motor, voltage=self.voltage)
        self.assertEqual(self.motor.details.count(), 1)

        with self.assertRaises(ProtectedError):
            motor_details.delete()
