from mixer.backend.django import mixer
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from builds.models import Drone
from components.models import Antenna


class TestDroneAPIView(BaseAPITest):

    def setUp(self):
        self.antenna1 = mixer.blend(Antenna)
        self.antenna2 = mixer.blend(Antenna)

        self.drone1 = mixer.blend(Drone,
                                  manufacturer='Manufacturer1',
                                  antenna=self.antenna1,)
        self.drone2 = mixer.blend(Drone,
                                  manufacturer='Manufacturer2',
                                  antenna=self.antenna2,)


    def test_list_drone(self):
        url = reverse('api:v1:builds:drone-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Drone.objects.all().count())

    def test_detail_drone(self):
        url = reverse('api:v1:builds:drone-detail', args={self.drone1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_drone(self):
        url = reverse('api:v1:builds:drone-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)

    def test_filter_drone(self):
        url = reverse('api:v1:builds:drone-list')
        response = self.client.get(url, {'antenna': self.antenna1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)

        response = self.client.get(url, {'antenna__center_frequency': 15})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)


