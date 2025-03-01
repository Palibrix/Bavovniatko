from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Gyro, SpeedControllerProtocol, FlightControllerFirmware, SpeedControllerFirmware, \
    RatedVoltage, FlightController, SpeedController, Stack
from galleries.models import FlightControllerGallery, SpeedControllerGallery, StackGallery
from suggestions.models import GyroSuggestion, SpeedControllerProtocolSuggestion, FlightControllerFirmwareSuggestion, \
    SpeedControllerFirmwareSuggestion, FlightControllerSuggestion, SpeedControllerSuggestion, StackSuggestion


class TestGyroSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")
        self.gyro_suggestion_1 = mixer.blend(GyroSuggestion,
                                           user=self.user_1,
                                           manufacturer='Test Manufacturer',
                                           imu='Test IMU',
                                           max_freq=8.0)
        self.gyro_suggestion_2 = mixer.blend(GyroSuggestion,
                                           manufacturer='Another Manufacturer',
                                           imu='Another IMU')

        self.create_data = {
            'manufacturer': 'New Manufacturer',
            'imu': 'New IMU',
            'max_freq': 8.0,
            'spi_support': True
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:gyro-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), GyroSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:gyro-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GyroSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.gyro_suggestion_1.refresh_from_db()
        self.assertEqual(self.gyro_suggestion_1.imu, self.create_data["imu"])

    def test_partial_update(self):
        update_data = {'imu': 'Updated IMU'}
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.gyro_suggestion_1.refresh_from_db()
        self.assertEqual(self.gyro_suggestion_1.imu, update_data["imu"])
        self.assertEqual(self.gyro_suggestion_1.max_freq, 8.0)

    def test_delete(self):
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:gyro-accept", args={self.gyro_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Gyro.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:gyro-accept", args={self.gyro_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Gyro.objects.count(), 1)
        self.gyro_suggestion_1.refresh_from_db()
        self.assertEqual(self.gyro_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid data"
        url = reverse("api:v1:suggestions:gyro-deny", args={self.gyro_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.gyro_suggestion_1.refresh_from_db()
        self.assertEqual(self.gyro_suggestion_1.status, 'denied')
        self.assertEqual(self.gyro_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.gyro_suggestion_1.status = 'approved'
        self.gyro_suggestion_1.save()

        update_data = {"imu": "New IMU"}
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.gyro_suggestion_1.status = 'denied'
        self.gyro_suggestion_1.save()

        update_data = {"imu": "New IMU"}
        url = reverse("api:v1:suggestions:gyro-detail", args={self.gyro_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.gyro_suggestion_1.refresh_from_db()
        self.assertEqual(self.gyro_suggestion_1.status, 'pending')


class TestSpeedControllerProtocolSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")
        self.protocol_suggestion_1 = mixer.blend(SpeedControllerProtocolSuggestion,
                                               user=self.user_1,
                                               protocol='Protocol 1')
        self.protocol_suggestion_2 = mixer.blend(SpeedControllerProtocolSuggestion,
                                               protocol='Protocol 2')

        self.create_data = {
            'protocol': 'New Protocol'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:sc_protocol-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                        SpeedControllerProtocolSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:sc_protocol-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SpeedControllerProtocolSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.protocol, self.create_data["protocol"])

    def test_partial_update(self):
        update_data = {'protocol': 'Updated Protocol'}
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.protocol, update_data["protocol"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:sc_protocol-accept", args={self.protocol_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SpeedControllerProtocol.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:sc_protocol-accept", args={self.protocol_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid protocol"
        url = reverse("api:v1:suggestions:sc_protocol-deny", args={self.protocol_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'denied')
        self.assertEqual(self.protocol_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.protocol_suggestion_1.status = 'approved'
        self.protocol_suggestion_1.save()

        update_data = {"protocol": "New Protocol"}
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.protocol_suggestion_1.status = 'denied'
        self.protocol_suggestion_1.save()

        update_data = {"protocol": "New Protocol"}
        url = reverse("api:v1:suggestions:sc_protocol-detail", args={self.protocol_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.protocol_suggestion_1.refresh_from_db()
        self.assertEqual(self.protocol_suggestion_1.status, 'pending')


class TestFlightControllerFirmwareSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")
        self.fc_firmware_suggestion_1 = mixer.blend(FlightControllerFirmwareSuggestion,
                                                  user=self.user_1,
                                                  firmware='Firmware 1')
        self.fc_firmware_suggestion_2 = mixer.blend(FlightControllerFirmwareSuggestion,
                                                  firmware='Firmware 2')

        self.create_data = {
            'firmware': 'New Firmware'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:fc_firmware-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                        FlightControllerFirmwareSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:fc_firmware-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlightControllerFirmwareSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.fc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_firmware_suggestion_1.firmware, self.create_data["firmware"])

    def test_partial_update(self):
        update_data = {'firmware': 'Updated Firmware'}
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.fc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_firmware_suggestion_1.firmware, update_data["firmware"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:fc_firmware-accept", args={self.fc_firmware_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FlightControllerFirmware.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:fc_firmware-accept", args={self.fc_firmware_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FlightControllerFirmware.objects.count(), 1)
        self.fc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_firmware_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid firmware"
        url = reverse("api:v1:suggestions:fc_firmware-deny", args={self.fc_firmware_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.fc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_firmware_suggestion_1.status, 'denied')
        self.assertEqual(self.fc_firmware_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.fc_firmware_suggestion_1.status = 'approved'
        self.fc_firmware_suggestion_1.save()

        update_data = {"firmware": "New Firmware"}
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.fc_firmware_suggestion_1.status = 'denied'
        self.fc_firmware_suggestion_1.save()

        update_data = {"firmware": "New Firmware"}
        url = reverse("api:v1:suggestions:fc_firmware-detail", args={self.fc_firmware_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.fc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_firmware_suggestion_1.status, 'pending')


class TestSpeedControllerFirmwareSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")
        self.esc_firmware_suggestion_1 = mixer.blend(SpeedControllerFirmwareSuggestion,
                                                  user=self.user_1,
                                                  firmware='Firmware 1')
        self.esc_firmware_suggestion_2 = mixer.blend(SpeedControllerFirmwareSuggestion,
                                                  firmware='Firmware 2')

        self.create_data = {
            'firmware': 'New Firmware'
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:sc_firmware-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                        SpeedControllerFirmwareSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:sc_firmware-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SpeedControllerFirmwareSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.esc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_firmware_suggestion_1.firmware, self.create_data["firmware"])

    def test_partial_update(self):
        update_data = {'firmware': 'Updated Firmware'}
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.esc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_firmware_suggestion_1.firmware, update_data["firmware"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:sc_firmware-accept", args={self.esc_firmware_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SpeedControllerFirmware.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:sc_firmware-accept", args={self.esc_firmware_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)
        self.esc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_firmware_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid firmware"
        url = reverse("api:v1:suggestions:sc_firmware-deny", args={self.esc_firmware_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.esc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_firmware_suggestion_1.status, 'denied')
        self.assertEqual(self.esc_firmware_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.esc_firmware_suggestion_1.status = 'approved'
        self.esc_firmware_suggestion_1.save()

        update_data = {"firmware": "New Firmware"}
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.esc_firmware_suggestion_1.status = 'denied'
        self.esc_firmware_suggestion_1.save()

        update_data = {"firmware": "New Firmware"}
        url = reverse("api:v1:suggestions:sc_firmware-detail", args={self.esc_firmware_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.esc_firmware_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_firmware_suggestion_1.status, 'pending')


class TestFlightControllerSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.gyro = mixer.blend(Gyro)
        self.voltage = mixer.blend(RatedVoltage)

        mixer.register(FlightControllerSuggestion,
                      description='TestFC',
                      voltage_min=2.0,
                      voltage_max=12.0,
                      mount_length=30.0,
                      mount_width=30.0,
                      weight=10.0,
                      length=35.0,
                      width=35.0)

        self.fc_suggestion_1 = mixer.blend(FlightControllerSuggestion,
                                         user=self.user_1,
                                         model='Test Model',
                                         manufacturer='Test Manufacturer',
                                         gyro=self.gyro,
                                         voltage=self.voltage)
        mixer.blend(FlightControllerGallery, suggestion=self.fc_suggestion_1)

        self.fc_suggestion_2 = mixer.blend(FlightControllerSuggestion)
        mixer.blend(FlightControllerGallery, suggestion=self.fc_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "microcontroller": "F7",
            "gyro": self.gyro.pk,
            "voltage": self.voltage.pk,
            "osd": "Test OSD",
            "bluetooth": True,
            "wifi": True,
            "barometer": True,
            "connector_type": "micro",
            "mount_length": 30.0,
            "mount_width": 30.0,
            "weight": 10.0,
            "length": 35.0,
            "width": 35.0,
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
        url = reverse("api:v1:suggestions:flight_controller-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), FlightControllerSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:flight_controller-detail", args={self.fc_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:flight_controller-detail", args={self.fc_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:flight_controller-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlightControllerGallery.objects.filter(suggestion=response.data['id']).count(), 1)

    def test_update(self):
        url = reverse("api:v1:suggestions:flight_controller-detail", args={self.fc_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.fc_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.fc_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:flight_controller-detail", args={self.fc_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.fc_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_suggestion_1.model, update_data["model"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:flight_controller-detail", args={self.fc_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:flight_controller-accept", args={self.fc_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FlightController.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:flight_controller-accept", args={self.fc_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FlightController.objects.count(), 1)
        self.fc_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid data"
        url = reverse("api:v1:suggestions:flight_controller-deny", args={self.fc_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.fc_suggestion_1.refresh_from_db()
        self.assertEqual(self.fc_suggestion_1.status, 'denied')
        self.assertEqual(self.fc_suggestion_1.admin_comment, comment)


class TestSpeedControllerSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.voltage = mixer.blend(RatedVoltage)

        mixer.register(SpeedControllerSuggestion,
                      description='TestESC',
                      voltage_min=2.0,
                      voltage_max=12.0,
                      cont_current=30.0,
                      burst_current=40.0,
                      mount_length=30.0,
                      mount_width=30.0,
                      weight=15.0,
                      length=35.0,
                      width=35.0)

        self.esc_suggestion_1 = mixer.blend(SpeedControllerSuggestion,
                                          user=self.user_1,
                                          model='Test Model',
                                          manufacturer='Test Manufacturer',
                                          voltage=self.voltage)
        mixer.blend(SpeedControllerGallery, suggestion=self.esc_suggestion_1)

        self.esc_suggestion_2 = mixer.blend(SpeedControllerSuggestion)
        mixer.blend(SpeedControllerGallery, suggestion=self.esc_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "voltage": self.voltage.pk,
            "is_wireless_conf": True,
            "esc_type": "all",
            "cont_current": 30.0,
            "burst_current": 40.0,
            "mount_length": 30.0,
            "mount_width": 30.0,
            "weight": 15.0,
            "length": 35.0,
            "width": 35.0,
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
        url = reverse("api:v1:suggestions:speed_controller-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), SpeedControllerSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:speed_controller-detail", args={self.esc_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:speed_controller-detail", args={self.esc_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:speed_controller-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SpeedControllerGallery.objects.filter(suggestion=response.data['id']).count(), 1)

    def test_update(self):
        url = reverse("api:v1:suggestions:speed_controller-detail", args={self.esc_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.esc_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.esc_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:speed_controller-detail", args={self.esc_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.esc_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_suggestion_1.model, update_data["model"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:speed_controller-detail", args={self.esc_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:speed_controller-accept", args={self.esc_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SpeedController.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:speed_controller-accept", args={self.esc_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SpeedController.objects.count(), 1)
        self.esc_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid data"
        url = reverse("api:v1:suggestions:speed_controller-deny", args={self.esc_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.esc_suggestion_1.refresh_from_db()
        self.assertEqual(self.esc_suggestion_1.status, 'denied')
        self.assertEqual(self.esc_suggestion_1.admin_comment, comment)


class TestStackSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.fc = mixer.blend(FlightController)
        self.esc = mixer.blend(SpeedController)

        mixer.register(StackSuggestion,
                      description='TestStack')

        self.stack_suggestion_1 = mixer.blend(StackSuggestion,
                                            user=self.user_1,
                                            model='Test Model',
                                            manufacturer='Test Manufacturer',
                                            flight_controller=self.fc,
                                            speed_controller=self.esc)
        mixer.blend(StackGallery, suggestion=self.stack_suggestion_1)

        self.stack_suggestion_2 = mixer.blend(StackSuggestion)
        mixer.blend(StackGallery, suggestion=self.stack_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "flight_controller": self.fc.pk,
            "speed_controller": self.esc.pk,
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
        url = reverse("api:v1:suggestions:stack-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), StackSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:stack-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(StackGallery.objects.filter(suggestion=response.data['id']).count(), 1)

    def test_update(self):
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.stack_suggestion_1.refresh_from_db()
        self.assertEqual(self.stack_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.stack_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.stack_suggestion_1.refresh_from_db()
        self.assertEqual(self.stack_suggestion_1.model, update_data["model"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:stack-accept", args={self.stack_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Stack.objects.count(), 0)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:stack-accept", args={self.stack_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Stack.objects.count(), 1)
        self.stack_suggestion_1.refresh_from_db()
        self.assertEqual(self.stack_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Invalid data"
        url = reverse("api:v1:suggestions:stack-deny", args={self.stack_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.stack_suggestion_1.refresh_from_db()
        self.assertEqual(self.stack_suggestion_1.status, 'denied')
        self.assertEqual(self.stack_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.stack_suggestion_1.status = 'approved'
        self.stack_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.stack_suggestion_1.status = 'denied'
        self.stack_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:stack-detail", args={self.stack_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.stack_suggestion_1.refresh_from_db()
        self.assertEqual(self.stack_suggestion_1.status, 'pending')
