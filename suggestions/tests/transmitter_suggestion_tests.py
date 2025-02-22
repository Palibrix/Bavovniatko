from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import Transmitter, OutputPower, VideoFormat
from documents.models import TransmitterDocument
from galleries.models import TransmitterGallery
from suggestions.models import TransmitterSuggestion, OutputPowerSuggestion
from users.tests import BaseUserTest


class TestTransmitterSuggestionModel(BaseUserTest):
    """Tests for TransmitterSuggestion with galleries, documents"""

    def setUp(self):
        mixer.register(TransmitterSuggestion,
                       description='TestTransmitter',
                       input_voltage_min=2,
                       input_voltage_max=10,
                       output_voltage=2)

        self.format1 = VideoFormat.objects.create(format='Format 1')
        self.format2 = VideoFormat.objects.create(format='Format 2')

        self.suggestion = mixer.blend(TransmitterSuggestion)
        self.suggestion.video_formats.add(self.format1, self.format2)

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(Transmitter.objects.count(), 0)
        self.assertTrue(self.suggestion.status, 'denied')

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(Transmitter.objects.count(), 1)
        self.assertTrue(self.suggestion.status, 'approved')
        transmitter = self.suggestion.related_instance
        self.assertEqual(transmitter.video_formats.count(), 2)

    def test_accept_suggestion_with_gallery(self):
        gallery = mixer.blend(TransmitterGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(TransmitterGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.delete()
        self.assertEqual(TransmitterGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(TransmitterGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.accept()
        self.suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(TransmitterGallery.objects.count(), 1)
        self.assertEqual(TransmitterSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        document = mixer.blend(TransmitterDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        document = mixer.blend(TransmitterDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.delete()
        self.assertEqual(TransmitterDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        document = mixer.blend(TransmitterDocument,
                               image=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        self.suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(TransmitterDocument.objects.count(), 1)
        self.assertEqual(TransmitterSuggestion.objects.count(), 0)

    def test_accept_multiple_times(self):
        self.suggestion.accept()
        self.assertEqual(Transmitter.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.suggestion.accept()
        self.assertEqual(Transmitter.objects.count(), 1)

    def test_images_become_accepted_after_suggestion_accepted(self):
        gallery = mixer.blend(TransmitterGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion,
                              accepted=False,
                              order=3)
        self.suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.suggestion.related_instance)


class TestOutputPowerSuggestionModel(BaseUserTest):

    def setUp(self):
        mixer.register(OutputPowerSuggestion)
        self.output_power_suggestion = mixer.blend(OutputPowerSuggestion)

    def test_deny(self):
        self.output_power_suggestion.deny()
        self.assertEqual(OutputPower.objects.count(), 0)
        self.assertTrue(self.output_power_suggestion.status, 'denied')

    def test_accept(self):
        self.output_power_suggestion.accept()
        self.assertEqual(OutputPower.objects.count(), 1)
        self.assertTrue(self.output_power_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.output_power_suggestion.accept()
        self.assertEqual(OutputPower.objects.count(), 1)
        self.output_power_suggestion.delete()
        self.assertEqual(OutputPower.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.output_power_suggestion.accept()
        self.assertEqual(OutputPower.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.output_power_suggestion.accept()
        self.assertEqual(OutputPower.objects.count(), 1)
