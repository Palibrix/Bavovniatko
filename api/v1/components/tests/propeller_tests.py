from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Propeller


class TestPropellerAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Propeller,
                       description='TestPropeller',
                       )

        self.propeller1 = mixer.blend(Propeller,
                                      manufacturer='Manufacturer1',
                                      blade_count=6
                                      )
        self.propeller2 = mixer.blend(Propeller,
                                      manufacturer='Manufacturer2',
                                      blade_count=2
                                      )

    def test_list_propeller(self):
        url = reverse('api:v1:components:propeller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Propeller.objects.all().count())

    def test_search_propeller(self):
        url = reverse('api:v1:components:propeller-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Propeller.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Propeller.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_propeller(self):
        url = reverse('api:v1:components:propeller-list')
        response = self.client.get(url, {'blade_count': 6})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('count'),
                         Propeller.objects.filter(blade_count=6).distinct().count())
