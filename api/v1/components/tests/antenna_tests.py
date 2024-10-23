from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Antenna, AntennaDetail, AntennaType


class TestAntennaAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Antenna,
                       description='TestAntenna',
                       bandwidth_min=1.0,
                       bandwidth_max=2.0,
                       center_frequency=1.5)
        self.antenna_type = mixer.blend(AntennaType)

        self.antenna1 = mixer.blend(Antenna, type=self.antenna_type,
                                    manufacturer='Manufacturer1',
                                    swr=2)
        self.antenna2 = mixer.blend(Antenna, type=self.antenna_type,
                                    manufacturer='Manufacturer2',
                                    swr=56)
        self.antenna1_detail_1 = mixer.blend(AntennaDetail, antenna=self.antenna1)
        self.antenna1_detail_2 = mixer.blend(AntennaDetail, antenna=self.antenna1)

    def test_list_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Antenna.objects.all().count())

    def test_detail_antenna(self):
        url = reverse('api:v1:components:antenna-detail', args={self.antenna1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['details']), AntennaDetail.objects.filter(antenna=self.antenna1).count())

    def test_search_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Antenna.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Antenna.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_antenna(self):
        url = reverse('api:v1:components:antenna-list')
        response = self.client.get(url, {'swr': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Antenna.objects.filter(swr=2).count())

        response = self.client.get(url, {'bandwidth_min': 1.0,
                                         'bandwidth_max': 2.0,
                                         'center_frequency': 1.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Antenna.objects.filter(bandwidth_min=1.0,
                                                bandwidth_max=2.0,
                                                center_frequency=1.5).count())
