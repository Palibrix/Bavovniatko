from unittest import TestCase

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from mixer.backend.django import mixer

from components.models import Frame, FrameCameraDetail


class TestFrameModel(TestCase):

    def setUp(self):
        mixer.register(Frame,
                       description='TestFrame',

                       )
        self.frame = mixer.blend(Frame,

                                  )

    def test_frame_delete_detail(self):
        mixer.cycle(2).blend(FrameCameraDetail, frame=self.frame)
        self.assertEqual(self.frame.camera_details.count(), 2)

        detail_to_delete = self.frame.camera_details.first()
        detail_to_delete.delete()

        self.assertEqual(self.frame.camera_details.count(), 1)

    def test_frame_delete_only_detail(self):
        frame_camera_detail = mixer.blend(FrameCameraDetail, frame=self.frame)
        self.assertEqual(self.frame.camera_details.count(), 1)

        with self.assertRaises(ProtectedError):
            frame_camera_detail.delete()
