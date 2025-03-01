from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Camera, VideoFormat, CameraDetail


class TestCameraAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Camera,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180)
        self.video_format = mixer.blend(VideoFormat)

        self.camera1 = mixer.blend(Camera, type=self.video_format,
                                   manufacturer='Manufacturer1',
                                   ratio='switch')
        self.camera2 = mixer.blend(Camera, type=self.video_format,
                                   manufacturer='Manufacturer2',
                                   ratio='another')
        self.camera1_detail_1 = mixer.blend(CameraDetail, camera=self.camera1)
        self.camera1_detail_2 = mixer.blend(CameraDetail, camera=self.camera1)

    def test_list_camera(self):
        url = reverse('api:v1:components:camera-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), Camera.objects.all().count())

    def test_detail_camera(self):
        url = reverse('api:v1:components:camera-detail', args={self.camera1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['details']), CameraDetail.objects.filter(camera=self.camera1).count())

    def test_search_camera(self):
        url = reverse('api:v1:components:camera-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Camera.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Camera.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_camera(self):
        url = reverse('api:v1:components:camera-list')
        response = self.client.get(url, {'ratio': 'switch'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Camera.objects.filter(ratio='switch').count())

        response = self.client.get(url, {'voltage_min': 2,
                                         'voltage_max': 10,
                                         'fov': 180
                                         }
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'),
                         Camera.objects.filter(voltage_min=2,
                                               voltage_max=10,
                                               fov=180).count())
