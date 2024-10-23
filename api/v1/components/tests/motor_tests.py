from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Motor, MotorDetail, RatedVoltage


class TestMotorAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Motor,
                       description='TestMotor',
                       stator_diameter='26',
                       stator_height='06',
                       )

        mixer.register(MotorDetail,
                       idle_current=10,
                       resistance=10,
                       weight=10
                       )

        self.motor1 = mixer.blend(Motor,
                                   manufacturer='Manufacturer1',
                                   )
        self.motor2 = mixer.blend(Motor,
                                   manufacturer='Manufacturer2',
                                   )

        self.voltage1 = mixer.blend(RatedVoltage, min_cells=6)

        self.motor1_detail_1 = mixer.blend(MotorDetail, motor=self.motor1, voltage=self.voltage1, peak_current=40)
        self.motor1_detail_2 = mixer.blend(MotorDetail, motor=self.motor1, voltage=self.voltage1, peak_current=90)
        self.motor2_detail_1 = mixer.blend(MotorDetail, motor=self.motor2, voltage=self.voltage1, peak_current=10)

    def test_list_motor(self):
        url = reverse('api:v1:components:motor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Motor.objects.all().count())

    def test_detail_motor(self):
        url = reverse('api:v1:components:motor-detail', args={self.motor1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['details']), MotorDetail.objects.filter(motor=self.motor1).count())

    def test_search_motor(self):
        url = reverse('api:v1:components:motor-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Motor.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Motor.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_motor(self):
        url = reverse('api:v1:components:motor-list')
        response = self.client.get(url, {'details__voltage__min_cells': 6})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data),
                         Motor.objects.filter(details__voltage__min_cells=6).distinct().count())

        response = self.client.get(url, {'details__voltage__min_cells': 6,
                                         'details__peak_current': 40,
                                         }
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Motor.objects.filter(details__voltage__min_cells=6,
                                               details__peak_current=40,
                                              ).distinct().count())
