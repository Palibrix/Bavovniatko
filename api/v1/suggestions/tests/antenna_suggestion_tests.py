import base64
import json

from django.db.models import Count
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import AntennaType, Antenna, AntennaConnector, AntennaDetail
from galleries.models import AntennaGallery
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_suggestions import SuggestedAntennaDetailSuggestion, AntennaTypeSuggestion, \
    AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion


class TestAntennaSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.user_2 = self.create(username="test2",
                                  email="test2@email.com")

        self.antenna = mixer.blend(Antenna)

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
                                                center_frequency=1.5,
                                                user=self.user_2)

        mixer.blend(AntennaGallery, suggestion=self.antenna_suggestion_2)
        self.type = mixer.blend(AntennaType)

        self.connector = mixer.blend(AntennaConnector, type="Connector1")

        self.antenna_1_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_1)
        self.antenna_1_detail_2 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_1)
        self.antenna_2_detail_1 = mixer.blend(SuggestedAntennaDetailSuggestion, suggestion=self.antenna_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 1",
            "description": "Description 1",
            "bandwidth_min": 2.0,
            "bandwidth_max": 4.0,
            "center_frequency": 3,
            "type_id": self.type.pk,
            "suggested_details": [
                {
                    "connector_type_id": 1,
                    "weight": 123,
                    "angle_type": "straight"
                },
                {
                    "connector_type_id": 1,
                    "weight": 1234,
                    "angle_type": "straight"
                },
            ],
            "suggested_images": [
                {
                    "image": base64.b64encode(self.create_image().read()),
                    "order": 1
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
        self.assertEqual(AntennaSuggestion.objects.count(), 3)
        self.assertEqual(AntennaGallery.objects.filter(suggestion=response.data['id']).count(), 1)

    def test_create_existing(self):
        create_data = self.create_data
        create_data.update({
            'related_instance_id': self.antenna.id,
            "model": "Suggestion to change model",
        })
        response = self.client.post(reverse("api:v1:suggestions:antenna-list"), data=create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AntennaSuggestion.objects.count(), 3)

    def test_update(self):
        update_data = {"model": "Model 1",
                       "manufacturer": "Manufacturer 2",
                       "description": "Description 1",
                       "bandwidth_min": 2.0,
                       "bandwidth_max": 4.0,
                       "center_frequency": 3,
                       "swr": 50,
                       "gain": 50,
                       "radiation": 50,
                       "type_id": self.type.pk,
                       "suggested_details": [
                           {
                               "connector_type_id": 1,
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
                               "order": 1
                           }
                       ],
                       'suggested_documents': [
                           {
                               'file': self.create_base64_pdf(),
                           }
                       ]
                       }
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.pk})
        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.antenna_suggestion_1.refresh_from_db()

        self.assertEqual(self.antenna_suggestion_1.gain, update_data["gain"])
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
                    'id': 2,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_partial_update_after_accept(self):
        self.antenna_suggestion_1.accept()

        update_data = {"model": "Completely new model"}
        url = reverse("api:v1:suggestions:antenna-detail", args={self.antenna_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.antenna_suggestion_1.refresh_from_db()

        self.assertFalse(self.antenna_suggestion_1.reviewed)
        self.assertFalse(self.antenna_suggestion_1.accepted)

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
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna-accept", args={self.antenna_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Antenna.objects.count(), 2)
        self.antenna_suggestion_1.refresh_from_db()
        self.assertTrue(self.antenna_suggestion_1.reviewed)
        self.assertTrue(self.antenna_suggestion_1.accepted)

    def test_accept_existing(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        existing_antenna_suggestion = mixer.blend(AntennaSuggestion,
                                                  user=self.user_1,
                                                  related_instance=self.antenna,
                                                  model='Suggestion to change model')

        url = reverse("api:v1:suggestions:antenna-accept", args={existing_antenna_suggestion.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Antenna.objects.count(), 1)
        existing_antenna_suggestion.refresh_from_db()
        self.assertTrue(existing_antenna_suggestion.reviewed)
        self.assertTrue(existing_antenna_suggestion.accepted)

    def test_deny(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        message = {
            'admin_comment': 'Denied because of a reason'
        }
        url = reverse("api:v1:suggestions:antenna-deny", args={self.antenna_suggestion_1.id})
        response = self.client.post(url, data=message)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Antenna.objects.count(), 1)
        self.antenna_suggestion_1.refresh_from_db()
        self.assertTrue(self.antenna_suggestion_1.reviewed)
        self.assertFalse(self.antenna_suggestion_1.accepted)
        self.assertEqual(self.antenna_suggestion_1.admin_comment, message['admin_comment'])


class TestAntennaTypeSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.user_2 = self.create(username="test2",
                                  email="test2@email.com")
        self.type_suggestion_1 = mixer.blend(AntennaTypeSuggestion,
                                             user=self.user_1,
                                             type='Type 1',
                                             direction='omni')
        self.type_suggestion_2 = mixer.blend(AntennaTypeSuggestion,
                                             user=self.user_2, )
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

    def test_create_existing(self):
        create_data = self.create_data
        create_data.update({
            'related_instance_id': self.type.id,
            "type": "Dipole",
        })
        url = reverse("api:v1:suggestions:antenna_type-list")
        response = self.client.post(url, data=create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AntennaTypeSuggestion.objects.count(), 3)
        self.assertEqual(AntennaTypeSuggestion.objects.filter(related_instance_id=self.type.id).count(), 1)

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

    def test_partial_update_after_accept(self):
        self.type_suggestion_1.accept()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_type-detail", args={self.type_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.type_suggestion_1.refresh_from_db()

        self.assertFalse(self.type_suggestion_1.reviewed)
        self.assertFalse(self.type_suggestion_1.accepted)

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
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_type-accept", args={self.type_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaType.objects.count(), 2)
        self.type_suggestion_1.refresh_from_db()
        self.assertTrue(self.type_suggestion_1.reviewed)
        self.assertTrue(self.type_suggestion_1.accepted)

    def test_accept_existing(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        existing_type_suggestion = mixer.blend(AntennaTypeSuggestion,
                                               user=self.user_1,
                                               related_instance=self.type,
                                               type='Suggestion to change type')

        url = reverse("api:v1:suggestions:antenna_type-accept", args={existing_type_suggestion.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaType.objects.count(), 1)

    def test_deny(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_type-deny", args={self.type_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaType.objects.count(), 1)
        self.type_suggestion_1.refresh_from_db()
        self.assertTrue(self.type_suggestion_1.reviewed)
        self.assertFalse(self.type_suggestion_1.accepted)


class TestAntennaConnectorSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.user_2 = self.create(username="test2",
                                  email="test2@email.com")
        self.connector_suggestion_1 = mixer.blend(AntennaConnectorSuggestion,
                                                  user=self.user_1,
                                                  type='Type 1')
        self.connector_suggestion_2 = mixer.blend(AntennaConnectorSuggestion,
                                                  user=self.user_2,
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

    def test_create_existing(self):
        create_data = self.create_data
        create_data.update({
            'related_instance_id': self.connector.id,
            "type": "New Type",
        })
        url = reverse("api:v1:suggestions:antenna_connector-list")
        response = self.client.post(url, data=create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AntennaConnectorSuggestion.objects.count(), 3)
        self.assertEqual(AntennaConnectorSuggestion.objects.filter(related_instance_id=1).count(), 1)

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

    def test_partial_update_after_accept(self):
        self.connector_suggestion_1.accept()

        update_data = {"type": "New Type"}
        url = reverse("api:v1:suggestions:antenna_connector-detail", args={self.connector_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.connector_suggestion_1.refresh_from_db()

        self.assertFalse(self.connector_suggestion_1.reviewed)
        self.assertFalse(self.connector_suggestion_1.accepted)

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
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_connector-accept", args={self.connector_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaConnector.objects.count(), 2)
        self.connector_suggestion_1.refresh_from_db()
        self.assertTrue(self.connector_suggestion_1.reviewed)
        self.assertTrue(self.connector_suggestion_1.accepted)

    def test_accept_existing(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        existing_type_suggestion = mixer.blend(AntennaConnectorSuggestion,
                                               user=self.user_1,
                                               related_instance=self.connector,
                                               type='Suggestion to change type')

        url = reverse("api:v1:suggestions:antenna_connector-accept", args={existing_type_suggestion.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaConnector.objects.count(), 1)

    def test_deny(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_connector-deny", args={self.connector_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaConnector.objects.count(), 1)
        self.connector_suggestion_1.refresh_from_db()
        self.assertTrue(self.connector_suggestion_1.reviewed)
        self.assertFalse(self.connector_suggestion_1.accepted)


class TestSuggestedAntennaDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.antenna = mixer.blend(Antenna)

        self.detail = mixer.blend(AntennaDetail, antenna=self.antenna)

        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.user_2 = self.create(username="test2",
                                  email="test2@email.com")
        self.detail_suggestion_1 = mixer.blend(ExistingAntennaDetailSuggestion,
                                               user=self.user_1,
                                               antenna=self.antenna)
        self.detail_suggestion_2 = mixer.blend(ExistingAntennaDetailSuggestion,
                                               user=self.user_2,
                                               antenna=self.antenna)
        self.connector = mixer.blend(AntennaConnector)

        self.create_data = {
            'antenna_id': self.antenna.pk,
            "connector_type_id": 1,
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

    def test_create_existing(self):
        create_data = self.create_data
        create_data.update({
            'related_instance_id': self.detail.id,
        })
        url = reverse("api:v1:suggestions:antenna_detail-list")
        response = self.client.post(url, data=create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingAntennaDetailSuggestion.objects.count(), 3)
        self.assertEqual(ExistingAntennaDetailSuggestion.objects.filter(related_instance_id=self.detail.id).count(), 1)

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

    def test_partial_update_after_accept(self):
        self.detail_suggestion_1.accept()

        update_data = {'weight': self.create_data["weight"]}
        url = reverse("api:v1:suggestions:antenna_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()

        self.assertFalse(self.detail_suggestion_1.reviewed)
        self.assertFalse(self.detail_suggestion_1.accepted)

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
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaDetail.objects.count(), 2)
        self.detail_suggestion_1.refresh_from_db()
        self.assertTrue(self.detail_suggestion_1.reviewed)
        self.assertTrue(self.detail_suggestion_1.accepted)

    def test_accept_existing(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        existing_detail_suggestion = mixer.blend(ExistingAntennaDetailSuggestion,
                                                 user=self.user_1,
                                                 related_instance=self.detail,
                                                 antenna=self.antenna,
                                                 weight=self.create_data["weight"])

        url = reverse("api:v1:suggestions:antenna_detail-accept", args={existing_detail_suggestion.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaDetail.objects.count(), 1)

    def test_deny(self):
        self.logout()
        superuser = self.create_super_user('test_superuser')
        self.authorize(superuser)

        url = reverse("api:v1:suggestions:antenna_detail-deny", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AntennaDetail.objects.count(), 1)
        self.detail_suggestion_1.refresh_from_db()
        self.assertTrue(self.detail_suggestion_1.reviewed)
        self.assertFalse(self.detail_suggestion_1.accepted)
