from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from mixer.backend.django import mixer

from components.models import Camera, CameraDetail


class TestCameraModel(TestCase):

    def setUp(self):
        mixer.register(Camera,
                       description='TestCamera',
                       fov=180
                       )
        self.camera = mixer.blend(Camera,
                                   voltage_min=2,
                                   voltage_max=10,
                                  )

    def test_camera_voltage_incorrect(self):
        with self.assertRaises(ValidationError):
            mixer.blend(Camera,
                        voltage_min=28,
                        voltage_max=10)

    def test_camera_delete_detail(self):
        mixer.cycle(2).blend(CameraDetail, camera=self.camera)
        self.assertEqual(self.camera.details.count(), 2)

        detail_to_delete = self.camera.details.first()
        detail_to_delete.delete()

        self.assertEqual(self.camera.details.count(), 1)

    def test_camera_delete_only_detail(self):
        camera_detail = mixer.blend(CameraDetail, camera=self.camera)
        self.assertEqual(self.camera.details.count(), 1)

        with self.assertRaises(ProtectedError):
            camera_detail.delete()
