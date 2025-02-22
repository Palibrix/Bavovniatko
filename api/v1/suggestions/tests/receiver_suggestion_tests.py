from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Receiver, ReceiverDetail, ReceiverProtocolType
from galleries.models import ReceiverGallery
from suggestions.models import (
    ReceiverSuggestion,
    ReceiverProtocolTypeSuggestion,
    ExistingReceiverDetailSuggestion,
    SuggestedReceiverDetailSuggestion
)


class TestReceiverProtocolTypeSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.protocol_suggestion_1 = mixer.blend(ReceiverProtocolTypeSuggestion,
                                                 user=self.user_1)
        self.protocol_suggestion_2 = mixer.blend(ReceiverProtocolTypeSuggestion)
        self.protocol = mixer.blend(ReceiverProtocolType)

        self.create_data = {
            'type': 'New Protocol'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ReceiverProtocolTypeSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ReceiverProtocolTypeSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.type, self.create_data["type"])

    def test_partial_update(self):
        update_data = {
            'type': self.create_data["type"],
        }
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.type, self.create_data["type"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:receiver_protocol_type-accept",
                      args={self.protocol_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:receiver_protocol_type-accept",
                      args={self.protocol_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ReceiverProtocolType.objects.count(), 2)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:receiver_protocol_type-deny",
                      args={self.protocol_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ReceiverProtocolType.objects.count(), 1)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'denied')

    def test_cannot_modify_approved_suggestion(self):
        self.protocol_suggestion_1.status = 'approved'
        self.protocol_suggestion_1.save()

        update_data = {"type": "New Protocol Type"}
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.protocol_suggestion_1.status = 'denied'
        self.protocol_suggestion_1.save()

        update_data = {"type": "New Protocol Type"}
        url = reverse("api:v1:suggestions:receiver_protocol_type-detail",
                      args={self.protocol_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'pending')


class TestReceiverSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        self.receiver = mixer.blend(Receiver)
        self.protocol = mixer.blend(ReceiverProtocolType)

        self.receiver_suggestion_1 = mixer.blend(ReceiverSuggestion,
                                                 user=self.user_1)
        mixer.blend(ReceiverGallery, suggestion=self.receiver_suggestion_1)

        self.receiver_suggestion_2 = mixer.blend(ReceiverSuggestion,
                                                 )
        mixer.blend(ReceiverGallery, suggestion=self.receiver_suggestion_2)

        self.receiver_1_detail_1 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                               suggestion=self.receiver_suggestion_1,
                                               frequency=433.0,
                                               weight=10.0,
                                               telemetry_power=1.0)
        self.receiver_1_detail_2 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                               suggestion=self.receiver_suggestion_1,
                                               frequency=866.0,
                                               weight=10.0,
                                               telemetry_power=1.0)
        self.receiver_2_detail_1 = mixer.blend(SuggestedReceiverDetailSuggestion,
                                               suggestion=self.receiver_suggestion_2,
                                               frequency=433.0,
                                               weight=10.0,
                                               telemetry_power=1.0)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "voltage_min": 5.0,
            "voltage_max": 12.0,
            "processor": "STM32F405",
            "protocols": [self.protocol.pk],
            "suggested_details": [
                {
                    "frequency": 433.0,
                    "weight": 10.0,
                    "telemetry_power": 1.0,
                    "rf_chip": "CC2500"
                }
            ],
            "suggested_images": [
                {
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                }
            ],
            "suggested_documents": [
                {
                    "file": self.create_base64_pdf()
                }
            ]
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:receiver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ReceiverSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_details"]),
                         SuggestedReceiverDetailSuggestion.objects.filter(
                             suggestion=self.receiver_suggestion_1).count())

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:receiver-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = ReceiverSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(ReceiverGallery.objects.filter(suggestion=response.data['id']).count(), 1)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.receiver_suggestion_1.refresh_from_db()
        self.assertEqual(self.receiver_suggestion_1.voltage_min, self.create_data["voltage_min"])
        self.assertEqual(self.receiver_suggestion_1.suggested_details.count(), 1)
        self.assertEqual(self.receiver_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.receiver_suggestion_1.refresh_from_db()
        self.assertEqual(self.receiver_suggestion_1.model, update_data["model"])

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("api:v1:suggestions:receiver-detail", args={self.receiver_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:receiver-accept", args={self.receiver_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Receiver.objects.count(), 1)
        self.assertEqual(ReceiverGallery.objects.filter(object__isnull=False).count(), 0)

    def test_accept(self):
        self.receiver_suggestion_1.protocols.add(self.protocol)

        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:receiver-accept", args={self.receiver_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Receiver.objects.count(), 2)
        self.receiver_suggestion_1.refresh_from_db()
        self.assertEqual(self.receiver_suggestion_1.status, 'approved')

        # Verify M2M fields are properly set
        receiver = self.receiver_suggestion_1.related_instance
        self.assertEqual(receiver.protocols.count(), 1)

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:receiver-deny", args={self.receiver_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.receiver_suggestion_1.refresh_from_db()
        self.assertEqual(self.receiver_suggestion_1.status, 'denied')
        self.assertEqual(self.receiver_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.receiver_suggestion_1.status = 'approved'
        self.receiver_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:receiver-detail",
                      args={self.receiver_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.receiver_suggestion_1.status = 'denied'
        self.receiver_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:receiver-detail",
                      args={self.receiver_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.receiver_suggestion_1.refresh_from_db()
        self.assertEqual(self.receiver_suggestion_1.status, 'pending')

    def test_images_become_accepted_after_suggestion_accepted(self):
        """Test that gallery images are marked as accepted after suggestion acceptance"""
        gallery = mixer.blend(ReceiverGallery,
                              image=self.create_image(),
                              suggestion=self.receiver_suggestion_1,
                              accepted=False,
                              order=3)
        url = reverse("api:v1:suggestions:receiver-accept", args={self.receiver_suggestion_1.id})
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)


class TestExistingReceiverDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.receiver = mixer.blend(Receiver)
        self.detail = mixer.blend(ReceiverDetail,
                                  receiver=self.receiver,
                                  frequency=1.0,
                                  weight=10.0,
                                  telemetry_power=1.0)

        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.detail_suggestion_1 = mixer.blend(ExistingReceiverDetailSuggestion,
                                               user=self.user_1,
                                               receiver=self.receiver,
                                               frequency=433.0,
                                               weight=10.0,
                                               telemetry_power=1.0)
        self.detail_suggestion_2 = mixer.blend(ExistingReceiverDetailSuggestion,
                                               receiver=self.receiver,
                                               frequency=866.0,
                                               weight=10.0,
                                               telemetry_power=1.0)

        self.create_data = {
            'receiver': self.receiver.pk,
            'frequency': 2.0,
            'weight': 10.0,
            'telemetry_power': 1.0,
            'rf_chip': 'CC2500'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:receiver_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ExistingReceiverDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:receiver_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:receiver_detail-detail", args={self.detail_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:receiver_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingReceiverDetailSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:receiver_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.frequency, self.create_data["frequency"])

    def test_partial_update(self):
        update_data = {'frequency': 866.0}
        url = reverse("api:v1:suggestions:receiver_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.frequency, update_data["frequency"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:receiver_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:receiver_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ReceiverDetail.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:receiver_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ReceiverDetail.objects.count(), 2)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:receiver_detail-deny", args={self.detail_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'denied')
        self.assertEqual(self.detail_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.detail_suggestion_1.status = 'approved'
        self.detail_suggestion_1.save()

        update_data = {"frequency": 866.0}
        url = reverse("api:v1:suggestions:receiver_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.detail_suggestion_1.status = 'denied'
        self.detail_suggestion_1.save()

        update_data = {"frequency": 866.0}
        url = reverse("api:v1:suggestions:receiver_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'pending')