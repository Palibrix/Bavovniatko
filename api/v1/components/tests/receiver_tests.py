from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Receiver, ReceiverProtocolType, ReceiverDetail, AntennaConnector


class TestReceiverAPIView(BaseAPITest):

    def setUp(self):
        self.protocol = mixer.blend(ReceiverProtocolType, )
        mixer.register(Receiver,
                       description='TestReceiver',
                       protocol=self.protocol,
                       )

        self.antenna_connector1 = mixer.blend(AntennaConnector, type='Type A')
        self.antenna_connector2 = mixer.blend(AntennaConnector, type='Type B')

        mixer.register(ReceiverDetail,
                       weight=10,
                       telemetry_power=10,
                       resistance=10,
                       )

        self.receiver1 = mixer.blend(Receiver,
                                     manufacturer='Manufacturer1',
                                     antenna_connectors=[self.antenna_connector1,],
                                     voltage_min=12.0,
                                     voltage_max=18.0,
                                     )
        self.receiver2 = mixer.blend(Receiver,
                                     manufacturer='Manufacturer2',
                                     antenna_connectors=[self.antenna_connector2,],
                                     voltage_min=12.0,
                                     voltage_max=18.0,
                                     )
        self.receiver1_detail_1 = mixer.blend(ReceiverDetail, receiver=self.receiver1, frequency=10)
        self.receiver1_detail_2 = mixer.blend(ReceiverDetail, receiver=self.receiver1, frequency=15)

    def test_list_receiver(self):
        url = reverse('api:v1:components:receiver-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Receiver.objects.all().count())

    def test_detail_receiver(self):
        url = reverse('api:v1:components:receiver-detail', args={self.receiver1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['details']), ReceiverDetail.objects.filter(receiver=self.receiver1).count())

    def test_search_receiver(self):
        url = reverse('api:v1:components:receiver-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Receiver.objects.filter(manufacturer__contains='Man').distinct().count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Receiver.objects.filter(manufacturer__contains='Manufacturer1').distinct().count())

    def test_filter_receiver(self):
        url = reverse('api:v1:components:receiver-list')
        response = self.client.get(url, {'antenna_connectors': ['Type A']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)
