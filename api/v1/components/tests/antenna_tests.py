from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector


class TestAntennaAPIView(BaseAPITest):

    def setUp(self):
        self.antenna_type = mixer.blend(AntennaType)

        self.antenna1 = mixer.blend(Antenna, type=self.antenna_type,
                                    manufacturer='Manufacturer1',
                                    swr=2, center_frequency=1.5)
        self.antenna2 = mixer.blend(Antenna, type=self.antenna_type,
                                    manufacturer='Manufacturer2',
                                    swr=56, center_frequency=15)
        self.connector1 = mixer.blend(AntennaConnector, type='Connector1')
        self.connector2 = mixer.blend(AntennaConnector, type='Connector2')

        self.antenna1_detail_1 = mixer.blend(AntennaDetail, antenna=self.antenna1, connector=self.connector1)
        self.antenna1_detail_2 = mixer.blend(AntennaDetail, antenna=self.antenna1, connector=self.connector2)
        self.antenna2_detail_1 = mixer.blend(AntennaDetail, antenna=self.antenna2, connector=self.connector2)

    def test_list_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Antenna.objects.all().count())

    def test_detail_antenna(self):
        url = reverse('api:v1:components:antenna-detail', args={self.antenna1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['details']), AntennaDetail.objects.filter(antenna=self.antenna1).count())

    def test_search_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Antenna.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Antenna.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url, {'swr': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)

        response = self.client.get(url, {'bandwidth_min': 1.0,
                                         'bandwidth_max': 20.0,
                                         'center_frequency_min': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)
