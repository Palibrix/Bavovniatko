from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Motor, MotorDetail, RatedVoltage
from galleries.models import MotorGallery
from suggestions.models import MotorSuggestion
from suggestions.models.motor_suggestion import (
    SuggestedMotorDetailSuggestion,
    RatedVoltageSuggestion,
    ExistingMotorDetailSuggestion
)


class TestMotorSuggestionAPIView(BaseAPITest):
    """Tests for the Motor Suggestion API endpoints"""
    def setUp(self):
        """Set up test data including users, suggestions, and required objects"""
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.motor = mixer.blend(Motor)
        self.voltage = mixer.blend(RatedVoltage)

        self.motor_suggestion_1 = mixer.blend(MotorSuggestion,
                                            stator_diameter='28',
                                            stator_height='06',
                                            configuration='12N14P',
                                            mount_height=30.5,
                                            mount_width=30.5,
                                            user=self.user_1,
                                            )
        mixer.blend(MotorGallery, suggestion=self.motor_suggestion_1)

        self.motor_suggestion_2 = mixer.blend(MotorSuggestion,
                                            stator_diameter='28',
                                            stator_height='06',
                                            configuration='12N14P')

        mixer.blend(MotorGallery, suggestion=self.motor_suggestion_2)

        self.motor_detail_1 = mixer.blend(SuggestedMotorDetailSuggestion,
                                      suggestion=self.motor_suggestion_1,
                                      voltage=self.voltage)
        self.motor_detail_2 = mixer.blend(SuggestedMotorDetailSuggestion,
                                      suggestion=self.motor_suggestion_1,
                                      voltage=self.voltage)
        self.other_detail_1 = mixer.blend(SuggestedMotorDetailSuggestion,
                                      suggestion=self.motor_suggestion_2,
                                      voltage=self.voltage)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "stator_diameter": "28",
            "stator_height": "06",
            "configuration": "12N14P",
            "mount_height": 30.5,
            "mount_width": 30.5,
            "suggested_details": [
                {
                    "weight": 50,
                    "max_power": 500,
                    "kv_per_volt": 2500,
                    "peak_current": 50,
                    "idle_current": 1.2,
                    "resistance": 0.15,
                    "voltage": self.voltage.pk
                },
                {
                    "weight": 48,
                    "max_power": 480,
                    "kv_per_volt": 2400,
                    "peak_current": 48,
                    "idle_current": 1.1,
                    "resistance": 0.14,
                    "voltage": self.voltage.pk
                }
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
        """Test retrieving list of motor suggestions"""
        url = reverse("api:v1:suggestions:motor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), MotorSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        """Test retrieving detail of a motor suggestion"""
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_details"]),
                        SuggestedMotorDetailSuggestion.objects.filter(suggestion=self.motor_suggestion_1).count())

    def test_detail_not_owner(self):
        """Test that users cannot access suggestions they don't own"""
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        """Test creating a new motor suggestion"""
        response = self.client.post(reverse("api:v1:suggestions:motor-list"), data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = MotorSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(MotorGallery.objects.filter(suggestion=response.data['id']).count(), 2)
        self.assertEqual(suggestion.status, 'pending')
        self.assertEqual(suggestion.suggested_details.count(), 2)

    def test_update(self):
        """Test updating an existing motor suggestion"""
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.motor_suggestion_1.refresh_from_db()

        self.assertEqual(self.motor_suggestion_1.mount_height, self.create_data["mount_height"])
        self.assertEqual(self.motor_suggestion_1.suggested_images.count(), 2)
        self.assertEqual(self.motor_suggestion_1.suggested_details.count(), 2)
        self.assertEqual(self.motor_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        """Test partial update of a motor suggestion"""
        update_data = {"model": "Completely new model",
                      "suggested_images": [
                          {
                              'id': 1,
                              "image": self.create_base64_image('test_test.jpg'),
                              "order": 1
                          },
                      ]}
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.motor_suggestion_1.refresh_from_db()
        self.assertEqual(self.motor_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.motor_suggestion_1.model, update_data["model"])
        self.assertEqual(self.motor_suggestion_1.stator_diameter, "28")

    def test_partial_update_wrong_image(self):
        """Test partial update with an invalid image id"""
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        """Test deleting a motor suggestion"""
        url = reverse("api:v1:suggestions:motor-detail", args={self.motor_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        """Test that non-admin users cannot accept suggestions"""
        url = reverse("api:v1:suggestions:motor-accept", args={self.motor_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Motor.objects.count(), 1)

    def test_accept(self):
        """Test accepting a suggestion by admin"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:motor-accept", args={self.motor_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Motor.objects.count(), 2)
        self.motor_suggestion_1.refresh_from_db()
        self.assertEqual(self.motor_suggestion_1.status, 'approved')
        self.assertEqual(Motor.objects.filter(id=self.motor_suggestion_1.related_instance.id).get().images.count(), 1)
        self.assertEqual(MotorGallery.objects.get(id=1).accepted, True)

    def test_deny(self):
        """Test denying a suggestion with admin comment"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        comment = "Needs more details"
        url = reverse("api:v1:suggestions:motor-deny",
                     args={self.motor_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)

        self.motor_suggestion_1.refresh_from_db()
        self.assertEqual(self.motor_suggestion_1.status, 'denied')
        self.assertEqual(self.motor_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.motor_suggestion_1.status = 'approved'
        self.motor_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:motor-detail",
                     args={self.motor_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.motor_suggestion_1.status = 'denied'
        self.motor_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:motor-detail",
                     args={self.motor_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.motor_suggestion_1.refresh_from_db()
        self.assertEqual(self.motor_suggestion_1.status, 'pending')

    def test_images_become_accepted_after_suggestion_accepted(self):
        """Test that gallery images are marked as accepted after suggestion acceptance"""
        gallery = mixer.blend(MotorGallery,
                            image=self.create_image(),
                            suggestion=self.motor_suggestion_1,
                            accepted=False,
                            order=3)
        url = reverse("api:v1:suggestions:motor-accept", args={self.motor_suggestion_1.id})
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)


class TestRatedVoltageSuggestionAPIView(BaseAPITest):
    """Tests for the Rated Voltage Suggestion API endpoints"""
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")
        self.voltage_suggestion_1 = mixer.blend(RatedVoltageSuggestion,
                                             user=self.user_1,
                                             min_cells=2,
                                             max_cells=6)
        self.voltage_suggestion_2 = mixer.blend(RatedVoltageSuggestion)
        self.voltage = mixer.blend(RatedVoltage)

        self.create_data = {
            'min_cells': 3,
            'max_cells': 8,
            'type': 'LIPO'
        }

    def test_list(self):
        """Test retrieving list of voltage suggestions"""
        url = reverse("api:v1:suggestions:rated_voltage-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), RatedVoltageSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        """Test retrieving detail of a voltage suggestion"""
        url = reverse("api:v1:suggestions:rated_voltage-detail", args={self.voltage_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        """Test that users cannot access suggestions they don't own"""
        url = reverse("api:v1:suggestions:rated_voltage-detail", args={self.voltage_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        """Test creating a new voltage suggestion"""
        url = reverse("api:v1:suggestions:rated_voltage-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RatedVoltageSuggestion.objects.count(), 3)

    def test_update(self):
        """Test updating an existing voltage suggestion"""
        url = reverse("api:v1:suggestions:rated_voltage-detail", args={self.voltage_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.voltage_suggestion_1.refresh_from_db()
        self.assertEqual(self.voltage_suggestion_1.min_cells, self.create_data["min_cells"])

    def test_partial_update(self):
        """Test partial update of a voltage suggestion"""
        update_data = {
            'min_cells': self.create_data["min_cells"],
        }
        url = reverse("api:v1:suggestions:rated_voltage-detail", args={self.voltage_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.voltage_suggestion_1.refresh_from_db()
        self.assertEqual(self.voltage_suggestion_1.min_cells, self.create_data["min_cells"])
        self.assertEqual(self.voltage_suggestion_1.max_cells, 6)

    def test_delete(self):
        """Test deleting a voltage suggestion"""
        url = reverse("api:v1:suggestions:rated_voltage-detail", args={self.voltage_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        """Test that non-admin users cannot accept suggestions"""
        url = reverse("api:v1:suggestions:rated_voltage-accept", args={self.voltage_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(RatedVoltage.objects.count(), 1)

    def test_accept(self):
        """Test accepting a suggestion by admin"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:rated_voltage-accept", args={self.voltage_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RatedVoltage.objects.count(), 2)
        self.voltage_suggestion_1.refresh_from_db()
        self.assertEqual(self.voltage_suggestion_1.status, 'approved')

    def test_deny(self):
        """Test denying a suggestion with admin comment"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        comment = "Invalid voltage range"
        url = reverse("api:v1:suggestions:rated_voltage-deny", args={self.voltage_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.voltage_suggestion_1.refresh_from_db()
        self.assertEqual(self.voltage_suggestion_1.status, 'denied')
        self.assertEqual(self.voltage_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.voltage_suggestion_1.status = 'approved'
        self.voltage_suggestion_1.save()

        update_data = {"min_cells": 4}
        url = reverse("api:v1:suggestions:rated_voltage-detail",
                     args={self.voltage_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.voltage_suggestion_1.status = 'denied'
        self.voltage_suggestion_1.save()

        update_data = {"min_cells": 4}
        url = reverse("api:v1:suggestions:rated_voltage-detail",
                     args={self.voltage_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.voltage_suggestion_1.refresh_from_db()
        self.assertEqual(self.voltage_suggestion_1.status, 'pending')


class TestExistingMotorDetailSuggestionAPIView(BaseAPITest):
    """Tests for the Existing Motor Detail Suggestion API endpoints"""
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1", email="test1@email.com")
        self.motor = mixer.blend(Motor)
        self.voltage = mixer.blend(RatedVoltage)

        self.motor_detail = mixer.blend(MotorDetail, motor=self.motor, voltage=self.voltage)

        self.suggestion_1 = mixer.blend(ExistingMotorDetailSuggestion,
                                      motor=self.motor,
                                      voltage=self.voltage,
                                      user=self.user_1)
        self.suggestion_2 = mixer.blend(ExistingMotorDetailSuggestion,
                                      motor=self.motor,
                                      voltage=self.voltage)

        self.create_data = {
            'motor': self.motor.pk,
            'voltage': self.voltage.pk,
            'weight': 50,
            'max_power': 500,
            'kv_per_volt': 2500,
            'peak_current': 50,
            'idle_current': 1.2,
            'resistance': 0.15
        }

    def test_list(self):
        """Test retrieving list of motor detail suggestions"""
        url = reverse("api:v1:suggestions:motor_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                        ExistingMotorDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        """Test retrieving detail of a motor detail suggestion"""
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        """Test that users cannot access suggestions they don't own"""
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        """Test creating a new motor detail suggestion"""
        url = reverse("api:v1:suggestions:motor_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingMotorDetailSuggestion.objects.count(), 3)

    def test_update(self):
        """Test updating an existing motor detail suggestion"""
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.weight, self.create_data["weight"])

    def test_partial_update(self):
        """Test partial update of a motor detail suggestion"""
        update_data = {'weight': 55.0}
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.weight, update_data["weight"])

    def test_delete(self):
        """Test deleting a motor detail suggestion"""
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        """Test that non-admin users cannot accept suggestions"""
        url = reverse("api:v1:suggestions:motor_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(MotorDetail.objects.count(), 1)

    def test_accept(self):
        """Test accepting a suggestion by admin"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:motor_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MotorDetail.objects.count(), 2)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'approved')

    def test_deny(self):
        """Test denying a suggestion with admin comment"""
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:motor_detail-deny", args={self.suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'denied')
        self.assertEqual(self.suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.suggestion_1.status = 'approved'
        self.suggestion_1.save()
        update_data = {"weight": 65.0}
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.suggestion_1.status = 'denied'
        self.suggestion_1.save()
        update_data = {"weight": 65.0}
        url = reverse("api:v1:suggestions:motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'pending')
