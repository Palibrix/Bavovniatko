from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import VideoFormat, Transmitter, OutputPower
from galleries.models import TransmitterGallery
from suggestions.models import TransmitterSuggestion, OutputPowerSuggestion


class TestTransmitterSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        self.transmitter = mixer.blend(Transmitter)
        self.format1 = mixer.blend(VideoFormat)

        self.transmitter_suggestion_1 = mixer.blend(TransmitterSuggestion,
                                                    input_voltage_min=5.0,
                                                    input_voltage_max=12.0,
                                                    output_voltage=5.0,
                                                    user=self.user_1,
                                                    )
        mixer.blend(TransmitterGallery, suggestion=self.transmitter_suggestion_1)

        self.transmitter_suggestion_2 = mixer.blend(TransmitterSuggestion,
                                                    input_voltage_min=5.0,
                                                    input_voltage_max=12.0,
                                                    output_voltage=5.0,
                                                    )
        mixer.blend(TransmitterGallery, suggestion=self.transmitter_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "input_voltage_min": 5.0,
            "input_voltage_max": 12.0,
            "output_voltage": 5.0,
            "channels_quantity": 8,
            "output": "A",
            "max_power": 1000,
            "microphone": True,
            "length": 50,
            "height": 30,
            "thickness": 10,
            "weight": 50,
            "video_formats": [self.format1.pk],
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
        url = reverse("api:v1:suggestions:transmitter-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), TransmitterSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        response = self.client.post(reverse("api:v1:suggestions:transmitter-list"), data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = TransmitterSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(TransmitterGallery.objects.filter(suggestion=response.data['id']).count(), 1)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.transmitter_suggestion_1.refresh_from_db()
        self.assertEqual(self.transmitter_suggestion_1.video_formats.count(), 1)
        self.assertEqual(self.transmitter_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.transmitter_suggestion_1.refresh_from_db()
        self.assertEqual(self.transmitter_suggestion_1.model, update_data["model"])

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("api:v1:suggestions:transmitter-detail", args={self.transmitter_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:transmitter-accept", args={self.transmitter_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Transmitter.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:transmitter-accept", args={self.transmitter_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transmitter.objects.count(), 2)
        self.transmitter_suggestion_1.refresh_from_db()
        self.assertEqual(self.transmitter_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:transmitter-deny", args={self.transmitter_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.transmitter_suggestion_1.refresh_from_db()
        self.assertEqual(self.transmitter_suggestion_1.status, 'denied')
        self.assertEqual(self.transmitter_suggestion_1.admin_comment, comment)


class TestOutputPowerSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.output_power_suggestion_1 = mixer.blend(OutputPowerSuggestion,
                                                     user=self.user_1)
        self.output_power_suggestion_2 = mixer.blend(OutputPowerSuggestion)
        self.output_power = mixer.blend(OutputPower)

        self.create_data = {
            'output_power': 1000,
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:output_power-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), OutputPowerSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:output_power-detail", args={self.output_power_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:output_power-detail", args={self.output_power_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:output_power-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(OutputPowerSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:output_power-detail", args={self.output_power_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.output_power_suggestion_1.refresh_from_db()
        self.assertEqual(self.output_power_suggestion_1.output_power, self.create_data["output_power"])

    def test_partial_update(self):
        update_data = {
            'output_power': self.create_data["output_power"],
        }
        url = reverse("api:v1:suggestions:output_power-detail", args={self.output_power_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.output_power_suggestion_1.refresh_from_db()
        self.assertEqual(self.output_power_suggestion_1.output_power, self.create_data["output_power"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:output_power-detail", args={self.output_power_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:output_power-accept", args={self.output_power_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(OutputPower.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:output_power-accept", args={self.output_power_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OutputPower.objects.count(), 2)
        self.output_power_suggestion_1.refresh_from_db()
        self.assertEqual(self.output_power_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid output power"
        url = reverse("api:v1:suggestions:output_power-deny", args={self.output_power_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.output_power_suggestion_1.refresh_from_db()
        self.assertEqual(self.output_power_suggestion_1.status, 'denied')
        self.assertEqual(self.output_power_suggestion_1.admin_comment, comment)