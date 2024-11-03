from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Frame, FrameVTXDetail, FrameMotorDetail, FrameCameraDetail


class TestFrameAPIView(BaseAPITest):

    def setUp(self):
        mixer.register(Frame,
                       description='TestFrame',
                       configuration='box'
                       )

        self.frame1 = mixer.blend(Frame,
                                  manufacturer='Manufacturer1',
                                  material='aluminum'
                                  )
        self.frame2 = mixer.blend(Frame,
                                  manufacturer='Manufacturer2',
                                  material='fibre',
                                  )

        self.frame1_camera_detail = mixer.blend(FrameCameraDetail, frame=self.frame1)
        self.frame1_motor_detail = mixer.blend(FrameMotorDetail, frame=self.frame1)
        self.frame1_vtx_detail = mixer.blend(FrameVTXDetail, frame=self.frame1)

    def test_list_frame(self):
        url = reverse('api:v1:components:frame-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Frame.objects.all().count())

    def test_detail_frame(self):
        url = reverse('api:v1:components:frame-detail', args={self.frame1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['camera_details']), FrameCameraDetail.objects.filter(frame=self.frame1).count())

    def test_search_frame(self):
        url = reverse('api:v1:components:frame-list')
        response = self.client.get(url, {'search': 'Man'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Frame.objects.filter(manufacturer__contains='Man').count())

        response = self.client.get(url, {'search': 'Manufacturer1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Frame.objects.filter(manufacturer__contains='Manufacturer1').count())

    def test_filter_frame(self):
        url = reverse('api:v1:components:frame-list')
        response = self.client.get(url, {'configuration': 'box'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Frame.objects.filter(configuration='box').count())

        response = self.client.get(url, {'configuration': 'box',
                                         'material': 'aluminum',
                                         }
                                   )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),
                         Frame.objects.filter(configuration='box',
                                              material='aluminum',
                                              ).count())
