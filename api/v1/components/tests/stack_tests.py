from django.db.models import Q
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import FlightController, Gyro, SpeedController, Stack, SpeedControllerProtocol


class TestStackAPIViews(BaseAPITest):

    def setUp(self):

        self.flight_controller1 = mixer.blend(FlightController,
                                              manufacturer='Manufacturer1',
                                              )
        self.speed_controller1 = mixer.blend(SpeedController,
                                              manufacturer='Manufacturer1',
                                              )

        self.speed_controller2 = mixer.blend(SpeedController,
                                             manufacturer='Manufacturer2',
                                             )


        self.stack1 = mixer.blend(Stack, flight_controller=self.flight_controller1,
                                  speed_controller=self.speed_controller1)
        self.stack2 = mixer.blend(Stack, flight_controller=self.flight_controller1,
                                  speed_controller=self.speed_controller2)

    def test_list_stack(self):
        url = reverse('api:v1:components:stack-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Stack.objects.all().count())

    def test_detail_stack(self):
        url = reverse('api:v1:components:stack-detail', args={self.stack1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_stack(self):
        url = reverse('api:v1:components:stack-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Stack.objects.filter(Q(manufacturer__contains='Man') |
                                              Q(flight_controller__manufacturer__contains='Man') |
                                              Q(speed_controller__manufacturer__contains='Man')).distinct().count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Stack.objects.filter(Q(manufacturer__contains='Manufacturer1') |
                                              Q(flight_controller__manufacturer__contains='Manufacturer1') |
                                              Q(speed_controller__manufacturer__contains='Manufacturer1')).distinct().count())

    def test_filter_stack(self):
        url = reverse('api:v1:components:stack-list')
        response = self.client.get(url, {'flight_controller_id': self.flight_controller1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Stack.objects.filter(flight_controller_id=self.flight_controller1.id).distinct().count())


class TestFlightControllerAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Stack,
                       description='TestStack',
                       )

        mixer.register(FlightController,
                       description='TestFlightController',
                       weight=15,
                       )

        self.gyro1 = mixer.blend(Gyro, imu='IMU_1')
        self.gyro2 = mixer.blend(Gyro, imu='IMU_2')

        self.flight_controller1 = mixer.blend(FlightController,
                                              manufacturer='Manufacturer1',
                                              gyro=self.gyro1,
                                              )
        self.flight_controller2 = mixer.blend(FlightController,
                                              manufacturer='Manufacturer2',
                                              gyro=self.gyro2,
                                              )
        self.stack = mixer.blend(Stack, flight_controller=self.flight_controller1)

    def test_list_flight_controller(self):
        url = reverse('api:v1:components:flight_controller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), FlightController.objects.all().count())

    def test_detail_flight_controller(self):
        url = reverse('api:v1:components:flight_controller-detail', args={self.flight_controller1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_flight_controller(self):
        url = reverse('api:v1:components:flight_controller-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         FlightController.objects.filter(manufacturer__contains='Man').distinct().count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         FlightController.objects.filter(manufacturer__contains='Manufacturer1').distinct().count())

    def test_filter_flight_controller(self):
        url = reverse('api:v1:components:flight_controller-list')
        response = self.client.get(url, {'gyro__imu': 'IMU_1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         FlightController.objects.filter(gyro__imu='IMU_1').distinct().count())

        response = self.client.get(url, {'in_stack': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         FlightController.objects.filter(stack__isnull=False).distinct().count())


class TestSpeedControllerAPIView(BaseAPITest):

    def setUp(self):

        self.protocol1 = mixer.blend(SpeedControllerProtocol, protocol='Protocol1')
        self.protocol2 = mixer.blend(SpeedControllerProtocol, protocol='Protocol2')

        self.speed_controller1 = mixer.blend(SpeedController,
                                             manufacturer='Manufacturer1',
                                             protocols=[self.protocol1, self.protocol2],
                                             )

        self.speed_controller2 = mixer.blend(SpeedController,
                                             manufacturer='Manufacturer2',
                                             protocols=[self.protocol1],
                                             burst_current=60
                                             )

    def test_list_speed_controller(self):
        url = reverse('api:v1:components:speed_controller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), SpeedController.objects.all().count())

    def test_detail_speed_controller(self):
        url = reverse('api:v1:components:speed_controller-detail', args={self.speed_controller1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_speed_controller(self):
        url = reverse('api:v1:components:speed_controller-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         SpeedController.objects.filter(manufacturer__contains='Man').distinct().count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         SpeedController.objects.filter(manufacturer__contains='Manufacturer1').distinct().count())

    def test_filter_speed_controller(self):
        url = reverse('api:v1:components:speed_controller-list')
        response = self.client.get(url, {'protocols': [self.protocol1.protocol, self.protocol2.protocol]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data['results'][0]['id'], self.speed_controller1.id)

        response = self.client.get(url, {'protocols': [self.protocol1.protocol]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 2)
        self.assertEqual(response.data['results'][1]['id'], self.speed_controller2.id)

    def test_filter_speed_controller_range(self):
        url = reverse('api:v1:components:speed_controller-list')
        response = self.client.get(url, {'burst_current_min': 40, 'burst_current_max': 80})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(response.data['results'][0]['id'], self.speed_controller2.id)