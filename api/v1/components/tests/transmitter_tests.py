from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Transmitter, OutputPower


class TestTransmitterAPIView(BaseAPITest):

    def setUp(self):
        self.output_power1 = mixer.blend(OutputPower, output_power=1300)
        self.output_power2 = mixer.blend(OutputPower, output_power=1500)

        self.transmitter1 = mixer.blend(Transmitter,
                                        manufacturer='Manufacturer1',
                                        output='A',
                                        output_powers=[self.output_power1])
        self.transmitter2 = mixer.blend(Transmitter,
                                        manufacturer='Manufacturer2',
                                        output='D',
                                        output_powers=[self.output_power1, self.output_power2])

    def test_list_transmitter(self):
        url = reverse('api:v1:components:transmitter-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Transmitter.objects.all().count())

    def test_detail_transmitter(self):
        url = reverse('api:v1:components:transmitter-detail', args={self.transmitter1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_transmitter(self):
        url = reverse('api:v1:components:transmitter-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)

    def test_filter_transmitter(self):
        url = reverse('api:v1:components:transmitter-list')
        response = self.client.get(url, {'output': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)

        response = self.client.get(url, {'output_powers': [self.output_power1.output_power, self.output_power2.output_power]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data['results'][0]['id'], self.transmitter2.id)
