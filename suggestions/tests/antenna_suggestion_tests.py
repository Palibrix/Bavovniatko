from mixer.backend.django import mixer

from components.models import Antenna, AntennaConnector, AntennaDetail, AntennaType
from documents.models import AntennaDocument
from galleries.models import AntennaGallery
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_suggestions import SuggestedAntennaDetailSuggestion, AntennaTypeSuggestion, \
    AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion
from users.tests import BaseUserTest


class TestAntennaSuggestionModel(BaseUserTest):
    """
    Tests for SuggestionAntenna with galleries, documents and details
    """

    def setUp(self):
        mixer.register(AntennaSuggestion,
                       description='TestAntenna',
                       )
        self.antenna_suggestion = mixer.blend(AntennaSuggestion,
                                              bandwidth_min=1.0,
                                              bandwidth_max=2.0,
                                              center_frequency=1.5)

        self.antenna_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion)
        self.antenna_detail_2 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion)

    def test_deny(self):
        self.antenna_suggestion.deny()
        self.assertEqual(Antenna.objects.count(), 0)
        self.assertFalse(self.antenna_suggestion.accepted)
        self.assertTrue(self.antenna_suggestion.reviewed)

    def test_accept(self):
        self.antenna_suggestion.accept()
        self.assertEqual(Antenna.objects.count(), 1)
        self.assertTrue(self.antenna_suggestion.accepted)
        self.assertTrue(self.antenna_suggestion.reviewed)


    def test_accept_suggestion_with_gallery(self):
        """
        Gallery creates connection to new object after suggestion is accepted
        """
        gallery = mixer.blend(AntennaGallery,
                              image=self.create_image(),
                              suggestion=self.antenna_suggestion)
        gallery.save()
        self.antenna_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.antenna_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        """
        Delete not accepted suggestion with gallery, gallery must be destroyed
        """
        gallery = mixer.blend(AntennaGallery,
                              image=self.create_image(),
                              suggestion=self.antenna_suggestion)
        gallery.save()
        self.antenna_suggestion.delete()
        self.assertEqual(AntennaGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """
        Delete accepted suggestion with gallery, gallery must remain in created instance
        """
        gallery = mixer.blend(AntennaGallery,
                              image=self.create_image(),
                              suggestion=self.antenna_suggestion)
        gallery.save()
        self.antenna_suggestion.accept()
        self.antenna_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(AntennaGallery.objects.count(), 1)
        self.assertEqual(AntennaSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """
        Document creates connection to new object after suggestion is accepted
        """
        document = mixer.blend(AntennaDocument,
                               file=self.create_image(),
                               suggestion=self.antenna_suggestion)
        document.save()
        self.antenna_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.antenna_suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """
        Delete not accepted suggestion with document, document must be destroyed
        """
        document = mixer.blend(AntennaDocument,
                               file=self.create_image(),
                               suggestion=self.antenna_suggestion)
        document.save()
        self.antenna_suggestion.delete()
        self.assertEqual(AntennaDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """
        Delete accepted suggestion with document, document must remain in created instance
        """
        document = mixer.blend(AntennaDocument,
                               image=self.create_image(),
                               suggestion=self.antenna_suggestion)
        document.save()
        self.antenna_suggestion.accept()
        self.antenna_suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(AntennaDocument.objects.count(), 1)
        self.assertEqual(AntennaSuggestion.objects.count(), 0)


class TestAntennaTypeSuggestionModel(BaseUserTest):
    """
    Tests for AntennaTypeSuggestion
    """

    def setUp(self):
        mixer.register(AntennaTypeSuggestion,
                       description='TestAntennaType',
                       )
        self.antenna_type_suggestion = mixer.blend(AntennaTypeSuggestion)

    def test_deny(self):
        self.antenna_type_suggestion.deny()
        self.assertEqual(AntennaType.objects.count(), 0)
        self.assertFalse(self.antenna_type_suggestion.accepted)
        self.assertTrue(self.antenna_type_suggestion.reviewed)

    def test_accept(self):
        self.antenna_type_suggestion.accept()
        self.assertEqual(AntennaType.objects.count(), 1)
        self.assertTrue(self.antenna_type_suggestion.accepted)
        self.assertTrue(self.antenna_type_suggestion.reviewed)

    def test_delete_accepted_suggestion(self):
        self.antenna_type_suggestion.accept()
        self.assertEqual(AntennaType.objects.count(), 1)
        self.antenna_type_suggestion.delete()
        self.assertEqual(AntennaType.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.antenna_type_suggestion.accept()
        self.assertEqual(AntennaType.objects.count(), 1)
        self.antenna_type_suggestion.accept()
        self.assertEqual(AntennaType.objects.count(), 1)


class TestAntennaConnectorSuggestionModel(BaseUserTest):
    """
    Tests for AntennaConnectorSuggestion
    """

    def setUp(self):
        mixer.register(AntennaConnectorSuggestion,
                       description='TestAntennaConnector',
                       )
        self.antenna_connector_suggestion = mixer.blend(AntennaConnectorSuggestion)

    def test_deny(self):
        self.antenna_connector_suggestion.deny()
        self.assertEqual(AntennaConnector.objects.count(), 0)
        self.assertFalse(self.antenna_connector_suggestion.accepted)
        self.assertTrue(self.antenna_connector_suggestion.reviewed)

    def test_accept(self):
        self.antenna_connector_suggestion.accept()
        self.assertEqual(AntennaConnector.objects.count(), 1)
        self.assertTrue(self.antenna_connector_suggestion.accepted)
        self.assertTrue(self.antenna_connector_suggestion.reviewed)

    def test_delete_accepted_suggestion(self):
        self.antenna_connector_suggestion.accept()
        self.assertEqual(AntennaConnector.objects.count(), 1)
        self.antenna_connector_suggestion.delete()
        self.assertEqual(AntennaConnector.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.antenna_connector_suggestion.accept()
        self.assertEqual(AntennaConnector.objects.count(), 1)
        self.antenna_connector_suggestion.accept()
        self.assertEqual(AntennaConnector.objects.count(), 1)


class TestExistingAntennaDetailSuggestionModel(BaseUserTest):
    """
    Tests for ExistingAntennaDetailSuggestion
    """

    def setUp(self):
        mixer.register(ExistingAntennaDetailSuggestion,
                       description='TestAntennaDetail',
                       )

        mixer.register(Antenna,
                       description='TestAntenna',
                       )
        self.antenna = mixer.blend(Antenna,
                                   bandwidth_min=1.0,
                                   bandwidth_max=2.0,
                                   center_frequency=1.5)

        self.antenna_detail_1 = mixer.blend(AntennaDetail, antenna=self.antenna)
        self.antenna_detail_2 = mixer.blend(AntennaDetail, antenna=self.antenna)

        self.antenna_detail_suggestion = mixer.blend(ExistingAntennaDetailSuggestion,
                                                     antenna=self.antenna)

    def test_deny(self):
        self.antenna_detail_suggestion.deny()
        self.assertEqual(AntennaDetail.objects.count(), 2)
        self.assertFalse(self.antenna_detail_suggestion.accepted)
        self.assertTrue(self.antenna_detail_suggestion.reviewed)

    def test_accept(self):
        self.antenna_detail_suggestion.accept()
        self.assertEqual(self.antenna.details.count(), 3)

        self.assertTrue(self.antenna_detail_suggestion.accepted)
        self.assertTrue(self.antenna_detail_suggestion.reviewed)

    def test_delete_accepted_suggestion(self):
        self.antenna_detail_suggestion.accept()
        self.antenna_detail_suggestion.delete()
        self.assertEqual(self.antenna.details.count(), 3)

    def test_accept_multiple_times(self):
        self.antenna_detail_suggestion.accept()
        self.assertEqual(self.antenna.details.count(), 3)
        self.antenna_detail_suggestion.accept()
        self.assertEqual(self.antenna.details.count(), 3)


class TestSuggestedAntennaDetailSuggestionModel(BaseUserTest):
    """
    Tests for SuggestedAntennaDetailSuggestion
    """

    def setUp(self):
        mixer.register(SuggestedAntennaDetailSuggestion,
                       description='TestAntenna',
                       )
        self.antenna_suggestion = mixer.blend(AntennaSuggestion,
                                              bandwidth_min=1.0,
                                              bandwidth_max=2.0,
                                              center_frequency=1.5)

        self.antenna_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion)
        self.antenna_detail_2 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion)

    def test_accept_details(self):
        self.antenna_suggestion.accept()
        self.assertEqual(AntennaDetail.objects.filter(antenna=self.antenna_suggestion.related_instance).count(),
                         2)

    def test_accept_details_multiple_times(self):
        """
        Accept suggestion with the created details must update details, not create new one
        """
        self.antenna_suggestion.accept()
        self.antenna_suggestion.accept()
        self.assertEqual(AntennaDetail.objects.filter(antenna=self.antenna_suggestion.related_instance).count(),
                         2)

    def test_deny(self):
        self.antenna_suggestion.deny()
        self.assertEqual(AntennaDetail.objects.count(), 0)

    def test_accept_delete_detail(self):
        """
        Delete detail from accepted suggestion, but it must remain in accepted suggestion
        """
        self.antenna_suggestion.accept()
        self.antenna_suggestion.refresh_from_db()
        self.assertEqual(Antenna.objects.count(), 1)
        self.antenna_detail_1.delete()

        remaining_details = AntennaDetail.objects.filter(antenna=self.antenna_suggestion.related_instance)
        self.assertEqual(remaining_details.count(), 2)
