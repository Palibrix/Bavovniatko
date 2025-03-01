from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import Receiver, ReceiverDetail, ReceiverProtocolType
from documents.models import ReceiverDocument
from galleries.models import ReceiverGallery
from suggestions.models import ReceiverSuggestion
from suggestions.models.receiver_suggestion import (
    SuggestedReceiverDetailSuggestion,
    ReceiverProtocolTypeSuggestion,
    ExistingReceiverDetailSuggestion
)
from users.tests import BaseUserTest


class TestReceiverSuggestionModel(BaseUserTest):
    """
    Tests for ReceiverSuggestion with galleries, documents and details
    """

    def setUp(self):
        mixer.register(ReceiverSuggestion,
                       description='TestReceiver',
                       voltage_min=5.0,
                       voltage_max=12.0)

        self.protocol1 = ReceiverProtocolType.objects.create(type='Protocol 1')
        self.protocol2 = ReceiverProtocolType.objects.create(type='Protocol 2')

        self.suggestion = mixer.blend(ReceiverSuggestion)
        self.suggestion.protocols.add(self.protocol1, self.protocol2)

        self.receiver_detail_1 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                             suggestion=self.suggestion,
                                             frequency=433.0,
                                             weight=10.0,
                                             telemetry_power=1.0)
        self.receiver_detail_2 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                             suggestion=self.suggestion,
                                             frequency=866.0,
                                             weight=10.0,
                                             telemetry_power=1.0)

    def test_deny(self):
        self.suggestion.deny()
        self.assertEqual(Receiver.objects.count(), 0)
        self.assertTrue(self.suggestion.status, 'denied')

    def test_accept(self):
        self.suggestion.accept()
        self.assertEqual(Receiver.objects.count(), 1)
        self.assertTrue(self.suggestion.status, 'accepted')
        receiver = self.suggestion.related_instance
        self.assertEqual(receiver.protocols.count(), 2)

    def test_accept_suggestion_with_gallery(self):
        """
        Gallery creates connection to new object after suggestion is accepted
        """
        gallery = mixer.blend(ReceiverGallery,
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
        gallery = mixer.blend(ReceiverGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.delete()
        self.assertEqual(ReceiverGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """
        Delete accepted suggestion with gallery, gallery must remain in created instance
        """
        gallery = mixer.blend(ReceiverGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion)
        gallery.save()
        self.suggestion.accept()
        self.suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(ReceiverGallery.objects.count(), 1)
        self.assertEqual(ReceiverSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """Document creates connection to new object after suggestion is accepted"""
        document = mixer.blend(ReceiverDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """Delete not accepted suggestion with document, document must be destroyed"""
        document = mixer.blend(ReceiverDocument,
                               file=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.delete()
        self.assertEqual(ReceiverDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """Delete accepted suggestion with document, document must remain in created instance"""
        document = mixer.blend(ReceiverDocument,
                               image=self.create_image(),
                               suggestion=self.suggestion)
        document.save()
        self.suggestion.accept()
        self.suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(ReceiverDocument.objects.count(), 1)
        self.assertEqual(ReceiverSuggestion.objects.count(), 0)

    def test_images_become_accepted_after_suggestion_accepted(self):
        """Gallery images should become accepted after suggestion is accepted"""
        gallery = mixer.blend(ReceiverGallery,
                              image=self.create_image(),
                              suggestion=self.suggestion,
                              accepted=False,
                              order=3)
        self.suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.suggestion.related_instance)


class TestReceiverProtocolTypeSuggestionModel(BaseUserTest):
    """Tests for ReceiverProtocolTypeSuggestion"""

    def setUp(self):
        mixer.register(ReceiverProtocolTypeSuggestion)
        self.protocol_suggestion = mixer.blend(ReceiverProtocolTypeSuggestion)

    def test_deny(self):
        self.protocol_suggestion.deny()
        self.assertEqual(ReceiverProtocolType.objects.count(), 0)
        self.assertTrue(self.protocol_suggestion.status, 'denied')

    def test_accept(self):
        self.protocol_suggestion.accept()
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)
        self.assertTrue(self.protocol_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.protocol_suggestion.accept()
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)
        self.protocol_suggestion.delete()
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.protocol_suggestion.accept()
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.protocol_suggestion.accept()


class TestExistingReceiverDetailSuggestionModel(BaseUserTest):
    """Tests for ExistingReceiverDetailSuggestion"""

    def setUp(self):
        mixer.register(ExistingReceiverDetailSuggestion,
                       frequency=1.0,
                       weight=10.0,
                       telemetry_power=1.0)

        mixer.register(Receiver,
                       description='TestReceiver',
                       voltage_min=5.0,
                       voltage_max=12.0)

        self.receiver = mixer.blend(Receiver)

        self.detail_1 = mixer.blend(ReceiverDetail,
                                    receiver=self.receiver,
                                    frequency=433.0,
                                    weight=10.0,
                                    telemetry_power=1.0)
        self.detail_2 = mixer.blend(ReceiverDetail,
                                    receiver=self.receiver,
                                    frequency=866.0,
                                    weight=10.0,
                                    telemetry_power=1.0)

        self.detail_suggestion = mixer.blend(ExistingReceiverDetailSuggestion,
                                             receiver=self.receiver)

    def test_deny(self):
        self.detail_suggestion.deny()
        self.assertEqual(ReceiverDetail.objects.count(), 2)
        self.assertTrue(self.detail_suggestion.status, 'denied')

    def test_accept(self):
        self.detail_suggestion.accept()
        self.assertEqual(self.receiver.details.count(), 3)
        self.assertTrue(self.detail_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.detail_suggestion.accept()
        self.detail_suggestion.delete()
        self.assertEqual(self.receiver.details.count(), 3)

    def test_accept_multiple_times(self):
        self.detail_suggestion.accept()
        self.assertEqual(self.receiver.details.count(), 3)
        with self.assertRaises(ValidationError):
            self.detail_suggestion.accept()


class TestSuggestedReceiverDetailSuggestionModel(BaseUserTest):
    """Tests for SuggestedReceiverDetailSuggestion"""

    def setUp(self):
        mixer.register(SuggestedReceiverDetailSuggestion,
                       weight=10.0,
                       telemetry_power=1.0)
        mixer.register(ReceiverSuggestion,
                       description='TestReceiverSuggestion',
                       voltage_min=5.0,
                       )

        self.receiver_suggestion = mixer.blend(ReceiverSuggestion)

        self.detail_1 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                    suggestion=self.receiver_suggestion,
                                    frequency=433.0,)
        self.detail_2 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                    suggestion=self.receiver_suggestion,
                                    frequency=866.0,)

    def test_accept_details(self):
        self.receiver_suggestion.accept()
        self.assertEqual(
            ReceiverDetail.objects.filter(receiver=self.receiver_suggestion.related_instance).count(), 2)

    def test_accept_details_multiple_times(self):
        self.receiver_suggestion.accept()
        with self.assertRaises(ValidationError):
            self.receiver_suggestion.accept()
        self.assertEqual(
            ReceiverDetail.objects.filter(receiver=self.receiver_suggestion.related_instance).count(), 2)

    def test_deny(self):
        self.receiver_suggestion.deny()
        self.assertEqual(ReceiverDetail.objects.count(), 0)

    def test_accept_delete_detail(self):
        """Delete detail from accepted suggestion, but it must remain in accepted suggestion"""
        self.receiver_suggestion.accept()
        self.receiver_suggestion.refresh_from_db()
        self.assertEqual(Receiver.objects.count(), 1)
        self.detail_1.delete()

        remaining_details = ReceiverDetail.objects.filter(
            receiver=self.receiver_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)
