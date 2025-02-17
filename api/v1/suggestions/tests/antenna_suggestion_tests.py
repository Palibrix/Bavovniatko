import base64
import json

from django.db.models import Count
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import AntennaType, Antenna, AntennaConnector, AntennaDetail
from galleries.models import AntennaGallery
from suggestions.models import AntennaSuggestion, SuggestedAntennaDetailSuggestion, AntennaTypeSuggestion, \
    AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion


class TestAntennaSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        self.antenna = mixer.blend(Antenna)
        self.type = mixer.blend(AntennaType)

        self.antenna_suggestion_1 = mixer.blend(AntennaSuggestion,
                                                bandwidth_min=1.0,
                                                bandwidth_max=2.0,
                                                center_frequency=1.5,
                                                user=self.user_1,
                                                )
        mixer.blend(AntennaGallery, suggestion=self.antenna_suggestion_1)

        self.antenna_suggestion_2 = mixer.blend(AntennaSuggestion,
                                                bandwidth_min=1.0,
                                                bandwidth_max=2.0,
                                                center_frequency=1.5)

        mixer.blend(AntennaGallery, suggestion=self.antenna_suggestion_2)

        self.connector = mixer.blend(AntennaConnector, type="Connector1")

        self.antenna_1_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_1)
        self.antenna_1_detail_2 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_1)
        self.antenna_2_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_2)

        self.create_data = {"model": "Model 1",
                            "manufacturer": "Manufacturer 2",
                            "description": "Description 1",
                            "bandwidth_min": 2.0,
                            "bandwidth_max": 4.0,
                            "center_frequency": 3,
                            "swr": 50,
                            "gain": 50,
                            "radiation": 50,
                            "type": self.type.pk,
                            "suggested_details": [
                                {
                                    "connector_type": 1,
                                    "weight": 123,
                                    "angle_type": "straight"
                                },
                            ],
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
        url = reverse("api:v1:suggestions:antenna-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), AntennaSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_details"]),
                         SuggestedAntennaDetailSuggestion.objects.filter(suggestion=self.antenna_suggestion_1).count())

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        response = self.client.post(reverse("api:v1:suggestions:antenna-list"), data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = AntennaSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(AntennaGallery.objects.filter(suggestion=response.data['id']).count(), 2)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.antenna_suggestion_1.refresh_from_db()

        self.assertEqual(self.antenna_suggestion_1.gain, self.create_data["gain"])
        self.assertEqual(self.antenna_suggestion_1.suggested_images.count(), 2)
        self.assertEqual(self.antenna_suggestion_1.suggested_details.count(), 1)
        self.assertEqual(self.antenna_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "Completely new model",
                       "suggested_images": [
                           {
                               'id': 1,
                               "image": self.create_base64_image('test_test.jpg'),
                               "order": 1
                           },
                       ]}
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.antenna_suggestion_1.refresh_from_db()
        self.assertEqual(self.antenna_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.antenna_suggestion_1.model, update_data["model"])
        self.assertEqual(self.antenna_suggestion_1.center_frequency, 1.5)

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:antenna-accept", args={self.antenna_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Antenna.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna-accept", args={self.antenna_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Antenna.objects.count(), 2)
        self.antenna_suggestion_1.refresh_from_db()
        self.assertEqual(self.antenna_suggestion_1.status, 'approved')
        self.assertEqual(Antenna.objects.filter(id=self.antenna_suggestion_1.related_instance.id).get().images.count(), 1)
        self.assertEqual(AntennaGallery.objects.get(id=1).accepted, True)

    def test_deny(self):
        """Test denying with admin comment"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        comment = "Needs more details"
        url = reverse("api:v1:suggestions:antenna-deny",
                      args={self.antenna_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)

        self.antenna_suggestion_1.refresh_from_db()
        self.assertEqual(self.antenna_suggestion_1.status, 'denied')
        self.assertEqual(self.antenna_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.antenna_suggestion_1.status = 'approved'
        self.antenna_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:antenna-detail",
                      args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.antenna_suggestion_1.status = 'denied'
        self.antenna_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:antenna-detail",
                      args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.antenna_suggestion_1.refresh_from_db()
        self.assertEqual(self.antenna_suggestion_1.status, 'pending')


class TestAntennaTypeSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.type_suggestion_1 = mixer.blend(AntennaTypeSuggestion,
                                             user=self.user_1,
                                             type='Type 1',
                                             direction='omni')
        self.type_suggestion_2 = mixer.blend(AntennaTypeSuggestion)
        self.type = mixer.blend(AntennaType)

        self.create_data = {
            'type': 'Monopole',
            'direction': 'omni',
            'polarization': 'linear'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:antenna_type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), AntennaTypeSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:antenna_type-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AntennaTypeSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.type_suggestion_1.refresh_from_db()
        self.assertEqual(self.type_suggestion_1.type, self.create_data["type"])

    def test_partial_update(self):
        update_data = {
            'type': self.create_data["type"],
        }
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.type_suggestion_1.refresh_from_db()
        self.assertEqual(self.type_suggestion_1.type, self.create_data["type"])
        self.assertEqual(self.type_suggestion_1.direction, 'omni')

    def test_delete(self):
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:antenna_type-accept", args={self.type_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(AntennaType.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna_type-accept", args={self.type_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaType.objects.count(), 2)
        self.type_suggestion_1.refresh_from_db()
        self.assertEqual(self.type_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna_type-deny", args={self.type_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaType.objects.count(), 1)
        self.type_suggestion_1.refresh_from_db()
        self.assertEqual(self.type_suggestion_1.status, 'denied')

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.type_suggestion_1.status = 'approved'
        self.type_suggestion_1.save()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_type-detail",
                      args={self.type_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.type_suggestion_1.status = 'denied'
        self.type_suggestion_1.save()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_type-detail",
                      args={self.type_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.type_suggestion_1.refresh_from_db()
        self.assertEqual(self.type_suggestion_1.status, 'pending')


class TestAntennaConnectorSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.connector_suggestion_1 = mixer.blend(AntennaConnectorSuggestion,
                                                  user=self.user_1,
                                                  type='Type 1')
        self.connector_suggestion_2 = mixer.blend(AntennaConnectorSuggestion,
                                                  type='Type 2')
        self.connector = mixer.blend(AntennaConnector)

        self.create_data = {
            'type': 'Type 3',
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:antenna_connector-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         AntennaConnectorSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:antenna_connector-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AntennaConnectorSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.connector_suggestion_1.refresh_from_db()
        self.assertEqual(self.connector_suggestion_1.type, self.create_data["type"])

    def test_partial_update(self):
        update_data = {
            'type': self.create_data["type"],
        }
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.connector_suggestion_1.refresh_from_db()
        self.assertEqual(self.connector_suggestion_1.type, self.create_data["type"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:antenna_connector-accept", args={self.connector_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(AntennaConnector.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna_connector-accept", args={self.connector_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaConnector.objects.count(), 2)
        self.connector_suggestion_1.refresh_from_db()
        self.assertTrue(self.connector_suggestion_1.status == 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna_connector-deny", args={self.connector_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaConnector.objects.count(), 1)
        self.connector_suggestion_1.refresh_from_db()
        self.assertTrue(self.connector_suggestion_1.status == 'denied')

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.connector_suggestion_1.status = 'approved'
        self.connector_suggestion_1.save()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_connector-detail",
                      args={self.connector_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.connector_suggestion_1.status = 'denied'
        self.connector_suggestion_1.save()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_connector-detail",
                      args={self.connector_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.connector_suggestion_1.refresh_from_db()
        self.assertEqual(self.connector_suggestion_1.status, 'pending')


class TestExistingAntennaDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.antenna = mixer.blend(Antenna)

        self.detail = mixer.blend(AntennaDetail, antenna=self.antenna)

        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.detail_suggestion_1 = mixer.blend(ExistingAntennaDetailSuggestion,
                                               user=self.user_1,
                                               antenna=self.antenna)
        self.detail_suggestion_2 = mixer.blend(ExistingAntennaDetailSuggestion,
                                               antenna=self.antenna)
        self.connector = mixer.blend(AntennaConnector)

        self.create_data = {
            'antenna': self.antenna.pk,
            "connector_type": 1,
            "weight": 123,
            "angle_type": "straight"
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:antenna_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ExistingAntennaDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:antenna_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingAntennaDetailSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.weight, self.create_data["weight"])

    def test_partial_update(self):
        update_data = {
            'weight': self.create_data["weight"],
        }
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.weight, self.create_data["weight"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:antenna_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(AntennaDetail.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:antenna_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaDetail.objects.count(), 2)
        self.detail_suggestion_1.refresh_from_db()
        self.assertTrue(self.detail_suggestion_1.status == 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:antenna_detail-deny", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaDetail.objects.count(), 1)
        self.detail_suggestion_1.refresh_from_db()
        self.assertTrue(self.detail_suggestion_1.status == 'denied')

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.detail_suggestion_1.status = 'approved'
        self.detail_suggestion_1.save()

        update_data = {"weight": 2145}
        url = reverse("api:v1:suggestions:antenna_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.detail_suggestion_1.status = 'denied'
        self.detail_suggestion_1.save()

        update_data = {"weight": 214235}
        url = reverse("api:v1:suggestions:antenna_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'pending')
