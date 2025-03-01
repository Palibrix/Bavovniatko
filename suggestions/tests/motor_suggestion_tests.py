from django.core.exceptions import ValidationError
from django.db import models
from mixer.backend.django import mixer

from components.models import Motor, MotorDetail, RatedVoltage
from documents.models import MotorDocument
from galleries.models import MotorGallery
from suggestions.models import MotorSuggestion
from suggestions.models.motor_suggestion import (
    SuggestedMotorDetailSuggestion,
    ExistingMotorDetailSuggestion,
    RatedVoltageSuggestion
)
from users.tests import BaseUserTest


class TestMotorSuggestionModel(BaseUserTest):
    """
    Tests for MotorSuggestion with galleries, documents and details
    """

    def setUp(self):
        mixer.register(MotorSuggestion,
                       description='TestMotor',
                       )
        self.voltage = mixer.blend(RatedVoltage)
        self.motor_suggestion = mixer.blend(MotorSuggestion,
                                            model='Test Model',
                                            manufacturer='Test Manufacturer',
                                            stator_diameter='28',
                                            stator_height='06',
                                            configuration='12N14P')

        self.motor_detail = mixer.blend(SuggestedMotorDetailSuggestion,
                                        suggestion=self.motor_suggestion,
                                        voltage=self.voltage,
                                        weight=12)
        self.motor_detail_2 = mixer.blend(SuggestedMotorDetailSuggestion,
                                          suggestion=self.motor_suggestion,
                                          voltage=self.voltage,
                                          weight=12)

    def test_deny(self):
        self.motor_suggestion.deny()
        self.assertEqual(Motor.objects.count(), 0)
        self.assertEqual(self.motor_suggestion.status, 'denied')

    def test_accept(self):
        self.motor_suggestion.accept()
        self.assertEqual(Motor.objects.count(), 1)
        self.assertEqual(self.motor_suggestion.status, 'approved')
        motor = self.motor_suggestion.related_instance
        self.assertEqual(motor.model, 'Test Model')
        self.assertEqual(motor.manufacturer, 'Test Manufacturer')

    def test_accept_suggestion_with_gallery(self):
        """Gallery creates connection to new object after suggestion is accepted"""
        gallery = mixer.blend(MotorGallery,
                              image=self.create_image(),
                              suggestion=self.motor_suggestion)
        gallery.save()
        self.motor_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.motor_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        """Delete not accepted suggestion with gallery, gallery must be destroyed"""
        gallery = mixer.blend(MotorGallery,
                              image=self.create_image(),
                              suggestion=self.motor_suggestion)
        gallery.save()
        self.motor_suggestion.delete()
        self.assertEqual(MotorGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """Delete accepted suggestion with gallery, gallery must remain in created instance"""
        gallery = mixer.blend(MotorGallery,
                              image=self.create_image(),
                              suggestion=self.motor_suggestion)
        gallery.save()
        self.motor_suggestion.accept()
        self.motor_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(MotorGallery.objects.count(), 1)
        self.assertEqual(MotorSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """Document creates connection to new object after suggestion is accepted"""
        document = mixer.blend(MotorDocument,
                               file=self.create_image(),
                               suggestion=self.motor_suggestion)
        document.save()
        self.motor_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.motor_suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """Delete not accepted suggestion with document, document must be destroyed"""
        document = mixer.blend(MotorDocument,
                               file=self.create_image(),
                               suggestion=self.motor_suggestion)
        document.save()
        self.motor_suggestion.delete()
        self.assertEqual(MotorDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """Delete accepted suggestion with document, document must remain in created instance"""
        document = mixer.blend(MotorDocument,
                               image=self.create_image(),
                               suggestion=self.motor_suggestion)
        document.save()
        self.motor_suggestion.accept()
        self.motor_suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(MotorDocument.objects.count(), 1)
        self.assertEqual(MotorSuggestion.objects.count(), 0)

    def test_accept_with_all_details(self):
        """Test that all details are properly created when suggestion is accepted"""
        self.motor_suggestion.accept()
        motor = self.motor_suggestion.related_instance
        self.assertEqual(motor.details.count(), 2)
        self.assertEqual(motor.details.first().voltage, self.voltage)

    def test_accept_multiple_times(self):
        """Test that suggestion cannot be accepted multiple times"""
        self.motor_suggestion.accept()
        self.assertEqual(Motor.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.motor_suggestion.accept()
        self.assertEqual(Motor.objects.count(), 1)

    def test_images_become_accepted_after_suggestion_accepted(self):
        """Gallery images should become accepted after suggestion is accepted"""
        gallery = mixer.blend(MotorGallery,
                              image=self.create_image(),
                              suggestion=self.motor_suggestion,
                              accepted=False,
                              order=3)
        self.motor_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.motor_suggestion.related_instance)


class TestRatedVoltageSuggestionModel(BaseUserTest):
    def setUp(self):
        mixer.register(RatedVoltageSuggestion)
        self.voltage_suggestion = mixer.blend(RatedVoltageSuggestion,
                                              min_cells=2,
                                              max_cells=6)

    def test_accept(self):
        self.voltage_suggestion.accept()
        self.assertEqual(RatedVoltage.objects.count(), 1)
        self.assertEqual(self.voltage_suggestion.status, 'approved')

    def test_deny(self):
        self.voltage_suggestion.deny()
        self.assertEqual(RatedVoltage.objects.count(), 0)
        self.assertEqual(self.voltage_suggestion.status, 'denied')

    def test_accept_multiple_times(self):
        self.voltage_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.voltage_suggestion.accept()
        self.assertEqual(RatedVoltage.objects.count(), 1)

    def test_delete_accepted_suggestion(self):
        self.voltage_suggestion.accept()
        self.voltage_suggestion.delete()
        self.assertEqual(RatedVoltage.objects.count(), 1)


class TestExistingMotorDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        mixer.register(MotorDetail, weight=1)
        mixer.register(ExistingMotorDetailSuggestion, weight=1)
        self.motor = mixer.blend(Motor,
                                 description='Test Motor',
                                 stator_diameter='28',
                                 stator_height='06')
        self.voltage = mixer.blend(RatedVoltage)
        self.motor_detail = mixer.blend(MotorDetail,
                                        motor=self.motor,
                                        voltage=self.voltage)
        self.suggestion = mixer.blend(ExistingMotorDetailSuggestion,
                                      motor=self.motor,
                                      voltage=self.voltage)

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(self.motor.details.count(), 2)
        self.assertEqual(self.suggestion.status, 'approved')

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(self.motor.details.count(), 1)
        self.assertEqual(self.suggestion.status, 'denied')

    def test_accept_multiple_times(self):
        self.suggestion.accept()
        with self.assertRaises(ValidationError):
            self.suggestion.accept()
        self.assertEqual(self.motor.details.count(), 2)

    def test_delete_accepted_suggestion(self):
        self.suggestion.accept()
        self.suggestion.delete()
        self.assertEqual(self.motor.details.count(), 2)

    def test_protected_delete(self):
        """Cannot delete the only motor detail"""
        with self.assertRaises(models.ProtectedError):
            self.motor_detail.delete()


class TestSuggestedMotorDetailSuggestionModel(BaseUserTest):
    def setUp(self):
        mixer.register(SuggestedMotorDetailSuggestion, weight=1)
        self.voltage = mixer.blend(RatedVoltage)
        self.motor_suggestion = mixer.blend(MotorSuggestion,
                                            description='Test Motor',
                                            stator_diameter='28',
                                            stator_height='06')
        self.motor_details = [
            mixer.blend(SuggestedMotorDetailSuggestion,
                        suggestion=self.motor_suggestion,
                        voltage=self.voltage)
            for _ in range(2)
        ]

    def test_accept_details(self):
        """Test that details are created when suggestion is accepted"""
        self.motor_suggestion.accept()
        motor = self.motor_suggestion.related_instance
        self.assertEqual(motor.details.count(), 2)

    def test_deny_details(self):
        """Test that no details are created when suggestion is denied"""
        self.motor_suggestion.deny()
        self.assertEqual(MotorDetail.objects.count(), 0)

    def test_delete_protection(self):
        """Test that the last detail cannot be deleted"""
        self.motor_details[0].delete()
        with self.assertRaises(models.ProtectedError):
            self.motor_details[1].delete()

    def test_accept_delete_detail(self):
        """Detail remains in accepted suggestion after deletion"""
        self.motor_suggestion.accept()
        self.motor_suggestion.refresh_from_db()
        self.assertEqual(Motor.objects.count(), 1)
        self.motor_details[1].delete()

        remaining_details = MotorDetail.objects.filter(motor=self.motor_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)

    def test_accept_details_multiple_times(self):
        """Accept suggestion with details must not create duplicate details"""
        self.motor_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.motor_suggestion.accept()
        motor = self.motor_suggestion.related_instance
        self.assertEqual(motor.details.count(), 2)
