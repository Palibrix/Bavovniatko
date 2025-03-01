from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Propeller
from galleries.models import PropellerGallery
from suggestions.models import PropellerSuggestion


class TestPropellerSuggestionAPIView(BaseAPITest):
    def setUp(self):
        mixer.register(Propeller, description='Test Description')
        mixer.register(PropellerSuggestion, description='Test Description')

        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.propeller = mixer.blend(Propeller)

        mixer.register(PropellerSuggestion,
                      description='TestPropeller')
        self.propeller_suggestion_1 = mixer.blend(PropellerSuggestion,
                                                model='Test Model',
                                                manufacturer='Test Manufacturer',
                                                size=5,
                                                pitch=4.5,
                                                user=self.user_1)

        mixer.blend(PropellerGallery, suggestion=self.propeller_suggestion_1)

        self.propeller_suggestion_2 = mixer.blend(PropellerSuggestion)

        mixer.blend(PropellerGallery, suggestion=self.propeller_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "size": 5,
            "pitch": 4.5,
            "blade_count": "2",
            "suggested_images": [
                {
                    'id': 1,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
                {
                    "image": self.create_base64_image('test_test2.jpg'),
                    "order": 2
                }
            ],
            'suggested_documents': [
                {
                    'file': self.create_base64_pdf(),
                }
            ]
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:propeller-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), PropellerSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:propeller-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = PropellerSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(PropellerGallery.objects.filter(suggestion=response.data['id']).count(), 2)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.propeller_suggestion_1.refresh_from_db()

        self.assertEqual(self.propeller_suggestion_1.suggested_images.count(), 2)
        self.assertEqual(self.propeller_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {
            "model": "Completely new model",
            "suggested_images": [
                {
                    'id': 1,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]
        }
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.propeller_suggestion_1.refresh_from_db()
        self.assertEqual(self.propeller_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.propeller_suggestion_1.model, update_data["model"])

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]
        }
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("api:v1:suggestions:propeller-detail", args={self.propeller_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:propeller-accept", args={self.propeller_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Propeller.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:propeller-accept", args={self.propeller_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Propeller.objects.count(), 2)
        self.propeller_suggestion_1.refresh_from_db()
        self.assertEqual(self.propeller_suggestion_1.status, 'approved')
        self.assertEqual(Propeller.objects.filter(
            id=self.propeller_suggestion_1.related_instance.id).get().images.count(), 1)
        self.assertEqual(PropellerGallery.objects.get(id=1).accepted, True)

    def test_deny(self):
        """Test denying with admin comment"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        comment = "Needs more details"
        url = reverse("api:v1:suggestions:propeller-deny",
                     args={self.propeller_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)

        self.propeller_suggestion_1.refresh_from_db()
        self.assertEqual(self.propeller_suggestion_1.status, 'denied')
        self.assertEqual(self.propeller_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.propeller_suggestion_1.status = 'approved'
        self.propeller_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:propeller-detail",
                     args={self.propeller_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.propeller_suggestion_1.status = 'denied'
        self.propeller_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:propeller-detail",
                     args={self.propeller_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.propeller_suggestion_1.refresh_from_db()
        self.assertEqual(self.propeller_suggestion_1.status, 'pending')