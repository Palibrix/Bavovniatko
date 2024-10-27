from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from mixer.backend.django import mixer

from components.models import Receiver, ReceiverProtocolType, ReceiverDetail


class TestReceiverModel(TestCase):

    def setUp(self):
        self.protocol = mixer.blend(ReceiverProtocolType, )
        mixer.register(Receiver,
                       description='TestReceiver',
                       protocol=self.protocol,
                       )

        mixer.register(ReceiverDetail,
                       weight=10,
                       telemetry_power=10,
                       resistance=10,
                       )
        self.receiver = mixer.blend(Receiver,
                                    voltage_min=12.0,
                                    voltage_max=18.0,
                                    )

    def test_voltage_incorrect(self):
        with self.assertRaises(ValidationError):
            mixer.blend(Receiver,
                        voltage_min=18.0,
                        voltage_max=12.0,
                        )

    def test_receiver_delete_detail(self):
        mixer.blend(ReceiverDetail, receiver=self.receiver, frequency=10)
        mixer.blend(ReceiverDetail, receiver=self.receiver, frequency=15)
        self.assertEqual(self.receiver.details.count(), 2)

        detail_to_delete = self.receiver.details.first()
        detail_to_delete.delete()

        self.assertEqual(self.receiver.details.count(), 1)

    def test_receiver_delete_only_detail(self):
        detail_to_delete = mixer.blend(ReceiverDetail, receiver=self.receiver, frequency=20)
        self.assertEqual(self.receiver.details.count(), 1)

        with self.assertRaises(ProtectedError):
            detail_to_delete.delete()
