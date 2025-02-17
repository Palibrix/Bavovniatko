from django.core.exceptions import ValidationError
from django.db import models
from mixer.backend.django import mixer

from components.models import Frame, FrameMotorDetail, FrameCameraDetail, FrameVTXDetail
from documents.models import FrameDocument
from galleries.models import FrameGallery
from suggestions.models import FrameSuggestion
from suggestions.models.frame_suggestion import (
    SuggestedFrameMotorDetailSuggestion,
    SuggestedFrameCameraDetailSuggestion,
    SuggestedFrameVTXDetailSuggestion,
    ExistingFrameMotorDetailSuggestion,
    ExistingFrameCameraDetailSuggestion,
    ExistingFrameVTXDetailSuggestion
)
from users.tests import BaseUserTest


class TestFrameSuggestionModel(BaseUserTest):
    """
    Tests for FrameSuggestion with galleries, documents and details
    """

    def setUp(self):
        mixer.register(FrameSuggestion,
                       description='TestFrame')
        self.frame_suggestion = mixer.blend(FrameSuggestion,
                                            model='Test Model',
                                            manufacturer='Test Manufacturer',
                                            prop_size='5 inch',
                                            size='220mm',
                                            material=Frame.MaterialChoice.FIBRE,
                                            configuration=Frame.ConfigurationChoice.X)

        self.camera_detail = mixer.blend(SuggestedFrameCameraDetailSuggestion,
                                         suggestion=self.frame_suggestion)
        self.motor_detail = mixer.blend(SuggestedFrameMotorDetailSuggestion,
                                        suggestion=self.frame_suggestion)
        self.vtx_detail = mixer.blend(SuggestedFrameVTXDetailSuggestion,
                                      suggestion=self.frame_suggestion)

    def test_deny(self):
        self.frame_suggestion.deny()
        self.assertEqual(Frame.objects.count(), 0)
        self.assertEqual(self.frame_suggestion.status, 'denied')

    def test_accept(self):
        self.frame_suggestion.accept()
        self.assertEqual(Frame.objects.count(), 1)
        self.assertEqual(self.frame_suggestion.status, 'approved')
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.model, 'Test Model')
        self.assertEqual(frame.manufacturer, 'Test Manufacturer')

    def test_accept_suggestion_with_gallery(self):
        """Gallery creates connection to new object after suggestion is accepted"""
        gallery = mixer.blend(FrameGallery,
                              image=self.create_image(),
                              suggestion=self.frame_suggestion)
        gallery.save()
        self.frame_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.frame_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        """Delete not accepted suggestion with gallery, gallery must be destroyed"""
        gallery = mixer.blend(FrameGallery,
                              image=self.create_image(),
                              suggestion=self.frame_suggestion)
        gallery.save()
        self.frame_suggestion.delete()
        self.assertEqual(FrameGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """Delete accepted suggestion with gallery, gallery must remain in created instance"""
        gallery = mixer.blend(FrameGallery,
                              image=self.create_image(),
                              suggestion=self.frame_suggestion)
        gallery.save()
        self.frame_suggestion.accept()
        self.frame_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(FrameGallery.objects.count(), 1)
        self.assertEqual(FrameSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """Document creates connection to new object after suggestion is accepted"""
        document = mixer.blend(FrameDocument,
                               file=self.create_image(),
                               suggestion=self.frame_suggestion)
        document.save()
        self.frame_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.frame_suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """Delete not accepted suggestion with document, document must be destroyed"""
        document = mixer.blend(FrameDocument,
                               file=self.create_image(),
                               suggestion=self.frame_suggestion)
        document.save()
        self.frame_suggestion.delete()
        self.assertEqual(FrameDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """Delete accepted suggestion with document, document must remain in created instance"""
        document = mixer.blend(FrameDocument,
                               image=self.create_image(),
                               suggestion=self.frame_suggestion)
        document.save()
        self.frame_suggestion.accept()
        self.frame_suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(FrameDocument.objects.count(), 1)
        self.assertEqual(FrameSuggestion.objects.count(), 0)

    def test_accept_with_all_details(self):
        """Test that all details are properly created when suggestion is accepted"""
        self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.camera_details.count(), 1)
        self.assertEqual(frame.motor_details.count(), 1)
        self.assertEqual(frame.vtx_details.count(), 1)

    def test_accept_multiple_times(self):
        """Test that suggestion cannot be accepted multiple times"""
        self.frame_suggestion.accept()
        self.assertEqual(Frame.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.frame_suggestion.accept()
        self.assertEqual(Frame.objects.count(), 1)

    def test_images_become_accepted_after_suggestion_accepted(self):
        """
        Gallery images should become accepted after suggestion is accepted
        """
        gallery = mixer.blend(FrameGallery,
                              image=self.create_image(),
                              suggestion=self.frame_suggestion,
                              accepted=False,
                              order=3)
        self.frame_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.frame_suggestion.related_instance)


class TestExistingFrameCameraDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame = mixer.blend(Frame,
                                 description='Test Frame',
                                 prop_size='5 inch',
                                 size='220mm')

        self.camera_detail = mixer.blend(FrameCameraDetail, frame=self.frame)
        self.suggestion = mixer.blend(ExistingFrameCameraDetailSuggestion,
                                      frame=self.frame)

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(self.frame.camera_details.count(), 2)
        self.assertEqual(self.suggestion.status, 'approved')

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(self.frame.camera_details.count(), 1)
        self.assertEqual(self.suggestion.status, 'denied')

    def test_accept_multiple_times(self):
        self.suggestion.accept()
        with self.assertRaises(ValidationError):
            self.suggestion.accept()
        self.assertEqual(self.frame.camera_details.count(), 2)

    def test_delete_accepted_suggestion(self):
        self.suggestion.accept()
        self.suggestion.delete()
        self.assertEqual(self.frame.camera_details.count(), 2)

    def test_protected_delete(self):
        """Cannot delete the only camera detail"""
        with self.assertRaises(models.ProtectedError):
            self.camera_detail.delete()


class TestSuggestedFrameCameraDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame_suggestion = mixer.blend(FrameSuggestion,
                                            description='Test Frame',
                                            prop_size='5 inch',
                                            size='220mm')
        self.camera_details = [
            mixer.blend(SuggestedFrameCameraDetailSuggestion, suggestion=self.frame_suggestion)
            for _ in range(2)
        ]

    def test_accept_details(self):
        """Test that details are created when suggestion is accepted"""
        self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.camera_details.count(), 2)

    def test_deny_details(self):
        """Test that no details are created when suggestion is denied"""
        self.frame_suggestion.deny()
        self.assertEqual(FrameCameraDetail.objects.count(), 0)

    def test_delete_protection(self):
        """Test that the last detail cannot be deleted"""
        self.camera_details[0].delete()
        with self.assertRaises(models.ProtectedError):
            self.camera_details[1].delete()

    def test_accept_delete_detail(self):
        """Detail remains in accepted suggestion after deletion"""
        self.frame_suggestion.accept()
        self.frame_suggestion.refresh_from_db()
        self.assertEqual(Frame.objects.count(), 1)
        self.camera_details[1].delete()

        remaining_details = FrameCameraDetail.objects.filter(frame=self.frame_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)

    def test_accept_details_multiple_times(self):
        """Accept suggestion with details must not create duplicate details"""
        self.frame_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.camera_details.count(), 2)


class TestExistingFrameMotorDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame = mixer.blend(Frame,
                                 description='Test Frame',
                                 prop_size='5 inch',
                                 size='220mm')

        self.motor_detail = mixer.blend(FrameMotorDetail, frame=self.frame)
        self.suggestion = mixer.blend(ExistingFrameMotorDetailSuggestion,
                                      frame=self.frame)

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(self.frame.motor_details.count(), 2)
        self.assertEqual(self.suggestion.status, 'approved')

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(self.frame.motor_details.count(), 1)
        self.assertEqual(self.suggestion.status, 'denied')

    def test_accept_multiple_times(self):
        self.suggestion.accept()
        with self.assertRaises(ValidationError):
            self.suggestion.accept()
        self.assertEqual(self.frame.motor_details.count(), 2)

    def test_delete_accepted_suggestion(self):
        self.suggestion.accept()
        self.suggestion.delete()
        self.assertEqual(self.frame.motor_details.count(), 2)

    def test_protected_delete(self):
        """Cannot delete the only motor detail"""
        with self.assertRaises(models.ProtectedError):
            self.motor_detail.delete()


class TestSuggestedFrameMotorDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame_suggestion = mixer.blend(FrameSuggestion,
                                            description='Test Frame',
                                            prop_size='5 inch',
                                            size='220mm')
        self.motor_details = [
            mixer.blend(SuggestedFrameMotorDetailSuggestion, suggestion=self.frame_suggestion)
            for _ in range(2)
        ]

    def test_accept_details(self):
        """Test that details are created when suggestion is accepted"""
        self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.motor_details.count(), 2)

    def test_deny_details(self):
        """Test that no details are created when suggestion is denied"""
        self.frame_suggestion.deny()
        self.assertEqual(FrameMotorDetail.objects.count(), 0)

    def test_delete_protection(self):
        """Test that the last detail cannot be deleted"""
        self.motor_details[0].delete()
        with self.assertRaises(models.ProtectedError):
            self.motor_details[1].delete()

    def test_accept_delete_detail(self):
        """Detail remains in accepted suggestion after deletion"""
        self.frame_suggestion.accept()
        self.frame_suggestion.refresh_from_db()
        self.assertEqual(Frame.objects.count(), 1)
        self.motor_details[1].delete()

        remaining_details = FrameMotorDetail.objects.filter(frame=self.frame_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)

    def test_accept_details_multiple_times(self):
        """Accept suggestion with details must not create duplicate details"""
        self.frame_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.motor_details.count(), 2)


class TestExistingFrameVTXDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame = mixer.blend(Frame,
                                 description='Test Frame',
                                 prop_size='5 inch',
                                 size='220mm')

        self.vtx_detail = mixer.blend(FrameVTXDetail, frame=self.frame)
        self.suggestion = mixer.blend(ExistingFrameVTXDetailSuggestion,
                                      frame=self.frame)

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(self.frame.vtx_details.count(), 2)
        self.assertEqual(self.suggestion.status, 'approved')

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(self.frame.vtx_details.count(), 1)
        self.assertEqual(self.suggestion.status, 'denied')

    def test_accept_multiple_times(self):
        self.suggestion.accept()
        with self.assertRaises(ValidationError):
            self.suggestion.accept()
        self.assertEqual(self.frame.vtx_details.count(), 2)

    def test_delete_accepted_suggestion(self):
        self.suggestion.accept()
        self.suggestion.delete()
        self.assertEqual(self.frame.vtx_details.count(), 2)

    def test_protected_delete(self):
        """Cannot delete the only VTX detail"""
        with self.assertRaises(models.ProtectedError):
            self.vtx_detail.delete()


class TestSuggestedFrameVTXDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        self.frame_suggestion = mixer.blend(FrameSuggestion,
                                            description='Test Frame',
                                            prop_size='5 inch',
                                            size='220mm')
        self.vtx_details = [
            mixer.blend(SuggestedFrameVTXDetailSuggestion, suggestion=self.frame_suggestion)
            for _ in range(2)
        ]

    def test_accept_details(self):
        """Test that details are created when suggestion is accepted"""
        self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.vtx_details.count(), 2)

    def test_deny_details(self):
        """Test that no details are created when suggestion is denied"""
        self.frame_suggestion.deny()
        self.assertEqual(FrameVTXDetail.objects.count(), 0)

    def test_delete_protection(self):
        """Test that the last detail cannot be deleted"""
        self.vtx_details[0].delete()
        with self.assertRaises(models.ProtectedError):
            self.vtx_details[1].delete()

    def test_accept_delete_detail(self):
        """Detail remains in accepted suggestion after deletion"""
        self.frame_suggestion.accept()
        self.frame_suggestion.refresh_from_db()
        self.assertEqual(Frame.objects.count(), 1)
        self.vtx_details[1].delete()

        remaining_details = FrameVTXDetail.objects.filter(frame=self.frame_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)

    def test_accept_details_multiple_times(self):
        """Accept suggestion with details must not create duplicate details"""
        self.frame_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.frame_suggestion.accept()
        frame = self.frame_suggestion.related_instance
        self.assertEqual(frame.vtx_details.count(), 2)