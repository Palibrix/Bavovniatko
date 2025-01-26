from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import Camera, CameraDetail, VideoFormat
from documents.models import CameraDocument
from galleries.models import CameraGallery
from suggestions.models import CameraSuggestion
from suggestions.models.camera_suggestion import SuggestedCameraDetailSuggestion, ExistingCameraDetailSuggestion, VideoFormatSuggestion
from users.tests import BaseUserTest


class TestCameraSuggestionModel(BaseUserTest):
    """
    Tests for SuggestionCamera with galleries, documents and details
    """

    def setUp(self):
        mixer.register(CameraSuggestion,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180)
        self.format1 = VideoFormat.objects.create(format='Format 1')
        self.format2 = VideoFormat.objects.create(format='Format 2')

        self.suggestion = mixer.blend(CameraSuggestion)
        self.suggestion.video_formats.add(self.format1, self.format2)

        self.camera_detail_1 = mixer.blend(SuggestedCameraDetailSuggestion, suggestion=self.suggestion)
        self.camera_detail_2 = mixer.blend(SuggestedCameraDetailSuggestion, suggestion=self.suggestion)


    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(Camera.objects.count(), 0)
        self.assertTrue(self.suggestion.status, 'denied')

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(Camera.objects.count(), 1)
        self.assertTrue(self.suggestion.status, 'accepted')
        camera = self.suggestion.related_instance
        self.assertEqual(camera.video_formats.count(), 2)

    def test_accept_suggestion_with_gallery(self):
        """
        Gallery creates connection to new object after suggestion is accepted
        """
        gallery = mixer.blend(CameraGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        """
        Delete not accepted suggestion with gallery, gallery must be destroyed
        """
        gallery = mixer.blend(CameraGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.delete()
        self.assertEqual(CameraGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """
        Delete accepted suggestion with gallery, gallery must remain in created instance
        """
        gallery = mixer.blend(CameraGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.accept()
        self.suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(CameraGallery.objects.count(), 1)
        self.assertEqual(CameraSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """
        Document creates connection to new object after suggestion is accepted
        """
        document = mixer.blend(CameraDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """
        Delete not accepted suggestion with document, document must be destroyed
        """
        document = mixer.blend(CameraDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.delete()
        self.assertEqual(CameraDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """
        Delete accepted suggestion with document, document must remain in created instance
        """
        document = mixer.blend(CameraDocument,
                               image=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        self.suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(CameraDocument.objects.count(), 1)
        self.assertEqual(CameraSuggestion.objects.count(), 0)


class TestVideoFormatSuggestionModel(BaseUserTest):
    """
    Tests for VideoFormatSuggestion
    """

    def setUp(self):
        mixer.register(VideoFormatSuggestion)
        self.video_format_suggestion = mixer.blend(VideoFormatSuggestion)

    def test_deny(self):
        self.video_format_suggestion.deny()
        self.assertEqual(VideoFormat.objects.count(), 0)
        self.assertTrue(self.video_format_suggestion.status, 'denied')

    def test_accept(self):
        self.video_format_suggestion.accept()
        self.assertEqual(VideoFormat.objects.count(), 1)
        self.assertTrue(self.video_format_suggestion.status, 'accepted')

    def test_delete_accepted_suggestion(self):
        self.video_format_suggestion.accept()
        self.assertEqual(VideoFormat.objects.count(), 1)
        self.video_format_suggestion.delete()
        self.assertEqual(VideoFormat.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.video_format_suggestion.accept()
        self.assertEqual(VideoFormat.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.video_format_suggestion.accept()
        

class TestExistingCameraDetailSuggestionModel(BaseUserTest):
    """
    Tests for ExistingCameraDetailSuggestion
    """

    def setUp(self):
        mixer.register(ExistingCameraDetailSuggestion,
                       description='TestCameraDetail',
                       )

        mixer.register(Camera,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180
                       )
        
        self.camera = mixer.blend(Camera)

        self.camera_detail_1 = mixer.blend(CameraDetail, camera=self.camera)
        self.camera_detail_2 = mixer.blend(CameraDetail, camera=self.camera)

        self.camera_detail_suggestion = mixer.blend(ExistingCameraDetailSuggestion,
                                                     camera=self.camera)

    def test_deny(self):
        self.camera_detail_suggestion.deny()
        self.assertEqual(CameraDetail.objects.count(), 2)
        self.assertTrue(self.camera_detail_suggestion.status, 'denied')

    def test_accept(self):
        self.camera_detail_suggestion.accept()
        self.assertEqual(self.camera.details.count(), 3)

        self.assertTrue(self.camera_detail_suggestion.status, 'accepted')

    def test_delete_accepted_suggestion(self):
        self.camera_detail_suggestion.accept()
        self.camera_detail_suggestion.delete()
        self.assertEqual(self.camera.details.count(), 3)

    def test_accept_multiple_times(self):
        self.camera_detail_suggestion.accept()
        self.assertEqual(self.camera.details.count(), 3)
        with self.assertRaises(ValidationError):
            self.camera_detail_suggestion.accept()
        

class TestSuggestedCameraDetailSuggestionModel(BaseUserTest):
    """
    Tests for SuggestedCameraDetailSuggestion
    """

    def setUp(self):
        mixer.register(CameraSuggestion,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180)
        self.camera_suggestion = mixer.blend(CameraSuggestion)

        self.camera_detail_1 = mixer.blend(SuggestedCameraDetailSuggestion, suggestion=self.camera_suggestion)
        self.camera_detail_2 = mixer.blend(SuggestedCameraDetailSuggestion, suggestion=self.camera_suggestion)

    def test_accept_details(self):
        self.camera_suggestion.accept()
        self.assertEqual(CameraDetail.objects.filter(camera=self.camera_suggestion.related_instance).count(),
                         2)

    def test_accept_details_multiple_times(self):
        self.camera_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.camera_suggestion.accept()
        self.assertEqual(CameraDetail.objects.filter(camera=self.camera_suggestion.related_instance).count(), 2)

    def test_deny(self):
        self.camera_suggestion.deny()
        self.assertEqual(CameraDetail.objects.count(), 0)

    def test_accept_delete_detail(self):
        """
        Delete detail from accepted suggestion, but it must remain in accepted suggestion
        """
        self.camera_suggestion.accept()
        self.camera_suggestion.refresh_from_db()
        self.assertEqual(Camera.objects.count(), 1)
        self.camera_detail_1.delete()

        remaining_details = CameraDetail.objects.filter(camera=self.camera_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)
