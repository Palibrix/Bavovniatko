from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import Propeller
from documents.models import PropellerDocument
from galleries.models import PropellerGallery
from suggestions.models import PropellerSuggestion
from users.tests import BaseUserTest


class TestPropellerSuggestionModel(BaseUserTest):
    """
    Tests for PropellerSuggestion with galleries and documents
    """
    def setUp(self):
        mixer.register(PropellerSuggestion,
                      description='TestPropeller')
        self.propeller_suggestion = mixer.blend(PropellerSuggestion,
                                              model='Test Model',
                                              manufacturer='Test Manufacturer',
                                              size=5,
                                              pitch=4.5,
                                              blade_count='2')

    def test_deny(self):
        self.propeller_suggestion.deny()
        self.assertEqual(Propeller.objects.count(), 0)
        self.assertTrue(self.propeller_suggestion.status, 'denied')

    def test_accept(self):
        self.propeller_suggestion.accept()
        self.assertEqual(Propeller.objects.count(), 1)
        self.assertTrue(self.propeller_suggestion.status, 'approved')

    def test_accept_suggestion_with_gallery(self):
        """
        Gallery creates connection to new object after suggestion is accepted
        """
        gallery = mixer.blend(PropellerGallery,
                            image=self.create_image(),
                            suggestion=self.propeller_suggestion)
        gallery.save()
        self.propeller_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.propeller_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        """
        Delete not accepted suggestion with gallery, gallery must be destroyed
        """
        gallery = mixer.blend(PropellerGallery,
                            image=self.create_image(),
                            suggestion=self.propeller_suggestion)
        gallery.save()
        self.propeller_suggestion.delete()
        self.assertEqual(PropellerGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        """
        Delete accepted suggestion with gallery, gallery must remain in created instance
        """
        gallery = mixer.blend(PropellerGallery,
                            image=self.create_image(),
                            suggestion=self.propeller_suggestion)
        gallery.save()
        self.propeller_suggestion.accept()
        self.propeller_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(PropellerGallery.objects.count(), 1)
        self.assertEqual(PropellerSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        """
        Document creates connection to new object after suggestion is accepted
        """
        document = mixer.blend(PropellerDocument,
                             file=self.create_image(),
                             suggestion=self.propeller_suggestion)
        document.save()
        self.propeller_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.propeller_suggestion.related_instance, document.object)

    def test_delete_not_accepted_suggestion_with_document(self):
        """
        Delete not accepted suggestion with document, document must be destroyed
        """
        document = mixer.blend(PropellerDocument,
                             file=self.create_image(),
                             suggestion=self.propeller_suggestion)
        document.save()
        self.propeller_suggestion.delete()
        self.assertEqual(PropellerDocument.objects.count(), 0)

    def test_delete_accepted_suggestion_with_document(self):
        """
        Delete accepted suggestion with document, document must remain in created instance
        """
        document = mixer.blend(PropellerDocument,
                             image=self.create_image(),
                             suggestion=self.propeller_suggestion)
        document.save()
        self.propeller_suggestion.accept()
        self.propeller_suggestion.delete()
        document.refresh_from_db()
        self.assertIsNone(document.suggestion)
        self.assertEqual(PropellerDocument.objects.count(), 1)
        self.assertEqual(PropellerSuggestion.objects.count(), 0)

    def test_images_become_accepted_after_suggestion_accepted(self):
        """
        Gallery images should become accepted after suggestion is accepted
        """
        gallery = mixer.blend(PropellerGallery,
                            image=self.create_image(),
                            suggestion=self.propeller_suggestion,
                            accepted=False,
                            order=3)
        self.propeller_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.propeller_suggestion.related_instance)

    def test_accept_multiple_times(self):
        self.propeller_suggestion.accept()
        self.assertEqual(Propeller.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.propeller_suggestion.accept()
        self.assertEqual(Propeller.objects.count(), 1)