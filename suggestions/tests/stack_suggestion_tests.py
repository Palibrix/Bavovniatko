from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from components.models import FlightController, Gyro, FlightControllerFirmware, SpeedControllerFirmware, \
    SpeedControllerProtocol, SpeedController, Stack
from documents.models import FlightControllerDocument, SpeedControllerDocument, StackDocument
from galleries.models import FlightControllerGallery, SpeedControllerGallery, StackGallery
from suggestions.models import FlightControllerSuggestion, FlightControllerFirmwareSuggestion, \
    SpeedControllerSuggestion, SpeedControllerFirmwareSuggestion, SpeedControllerProtocolSuggestion, StackSuggestion, \
    GyroSuggestion
from users.tests import BaseUserTest


class TestFlightControllerSuggestionModel(BaseUserTest):
    """Tests for FlightControllerSuggestion with galleries, documents and details"""

    def setUp(self):
        self.gyro = mixer.blend(Gyro)
        self.firmware1 = mixer.blend(FlightControllerFirmware)
        self.firmware2 = mixer.blend(FlightControllerFirmware)

        mixer.register(FlightControllerSuggestion,
                      description='TestFC',
                      voltage_min=2.0,
                      voltage_max=12.0,
                      mount_length=30.0,
                      mount_width=30.0,
                      weight=10.0,
                      length=35.0,
                      width=35.0)

        self.fc_suggestion = mixer.blend(FlightControllerSuggestion,
                                         model='Test Model',
                                         manufacturer='Test Manufacturer',
                                         gyro=self.gyro)

        self.fc_suggestion.firmwares.add(self.firmware1, self.firmware2)

    def test_deny(self):
        self.fc_suggestion.deny()
        self.assertEqual(FlightController.objects.count(), 0)
        self.assertEqual(self.fc_suggestion.status, 'denied')

    def test_accept(self):
        self.fc_suggestion.accept()
        self.assertEqual(FlightController.objects.count(), 1)
        self.assertEqual(self.fc_suggestion.status, 'approved')
        fc = self.fc_suggestion.related_instance
        self.assertEqual(fc.firmwares.count(), 2)

    def test_accept_suggestion_with_gallery(self):
        gallery = mixer.blend(FlightControllerGallery,
                              image=self.create_image(),
                              suggestion=self.fc_suggestion)
        gallery.save()
        self.fc_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.fc_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(FlightControllerGallery,
                              image=self.create_image(),
                              suggestion=self.fc_suggestion)
        gallery.save()
        self.fc_suggestion.delete()
        self.assertEqual(FlightControllerGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(FlightControllerGallery,
                              image=self.create_image(),
                              suggestion=self.fc_suggestion)
        gallery.save()
        self.fc_suggestion.accept()
        self.fc_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(FlightControllerGallery.objects.count(), 1)
        self.assertEqual(FlightControllerSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        document = mixer.blend(FlightControllerDocument,
                               file=self.create_image(),
                               suggestion=self.fc_suggestion)
        document.save()
        self.fc_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.fc_suggestion.related_instance, document.object)

    def test_images_become_accepted_after_suggestion_accepted(self):
        gallery = mixer.blend(FlightControllerGallery,
                              image=self.create_image(),
                              suggestion=self.fc_suggestion,
                              accepted=False,
                              order=3)
        self.fc_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.fc_suggestion.related_instance)

    def test_accept_multiple_times(self):
        self.fc_suggestion.accept()
        self.assertEqual(FlightController.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.fc_suggestion.accept()
        self.assertEqual(FlightController.objects.count(), 1)


class TestSpeedControllerSuggestionModel(BaseUserTest):
    """Tests for SpeedControllerSuggestion with galleries, documents and details"""

    def setUp(self):
        self.firmware1 = mixer.blend(SpeedControllerFirmware)
        self.firmware2 = mixer.blend(SpeedControllerFirmware)
        self.protocol1 = mixer.blend(SpeedControllerProtocol)
        self.protocol2 = mixer.blend(SpeedControllerProtocol)

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

        self.esc_suggestion = mixer.blend(SpeedControllerSuggestion,
                                          model='Test Model',
                                          manufacturer='Test Manufacturer')

        self.esc_suggestion.firmwares.add(self.firmware1, self.firmware2)
        self.esc_suggestion.protocols.add(self.protocol1, self.protocol2)

    def test_deny(self):
        self.esc_suggestion.deny()
        self.assertEqual(SpeedController.objects.count(), 0)
        self.assertEqual(self.esc_suggestion.status, 'denied')

    def test_accept(self):
        self.esc_suggestion.accept()
        self.assertEqual(SpeedController.objects.count(), 1)
        self.assertEqual(self.esc_suggestion.status, 'approved')
        esc = self.esc_suggestion.related_instance
        self.assertEqual(esc.firmwares.count(), 2)
        self.assertEqual(esc.protocols.count(), 2)

    def test_accept_suggestion_with_gallery(self):
        gallery = mixer.blend(SpeedControllerGallery,
                              image=self.create_image(),
                              suggestion=self.esc_suggestion)
        gallery.save()
        self.esc_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.esc_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(SpeedControllerGallery,
                              image=self.create_image(),
                              suggestion=self.esc_suggestion)
        gallery.save()
        self.esc_suggestion.delete()
        self.assertEqual(SpeedControllerGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(SpeedControllerGallery,
                              image=self.create_image(),
                              suggestion=self.esc_suggestion)
        gallery.save()
        self.esc_suggestion.accept()
        self.esc_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(SpeedControllerGallery.objects.count(), 1)
        self.assertEqual(SpeedControllerSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        document = mixer.blend(SpeedControllerDocument,
                               file=self.create_image(),
                               suggestion=self.esc_suggestion)
        document.save()
        self.esc_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.esc_suggestion.related_instance, document.object)

    def test_images_become_accepted_after_suggestion_accepted(self):
        gallery = mixer.blend(SpeedControllerGallery,
                              image=self.create_image(),
                              suggestion=self.esc_suggestion,
                              accepted=False,
                              order=3)
        self.esc_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.esc_suggestion.related_instance)

    def test_accept_multiple_times(self):
        self.esc_suggestion.accept()
        self.assertEqual(SpeedController.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.esc_suggestion.accept()
        self.assertEqual(SpeedController.objects.count(), 1)


class TestSpeedControllerFirmwareSuggestionModel(BaseUserTest):
    """Tests for ESC Firmware suggestions"""

    def setUp(self):
        mixer.register(SpeedControllerFirmwareSuggestion)
        self.firmware_suggestion = mixer.blend(SpeedControllerFirmwareSuggestion)

    def test_deny(self):
        self.firmware_suggestion.deny()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 0)
        self.assertEqual(self.firmware_suggestion.status, 'denied')

    def test_accept(self):
        self.firmware_suggestion.accept()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)
        self.assertEqual(self.firmware_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.firmware_suggestion.accept()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)
        self.firmware_suggestion.delete()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.firmware_suggestion.accept()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.firmware_suggestion.accept()
        self.assertEqual(SpeedControllerFirmware.objects.count(), 1)


class TestSpeedControllerProtocolSuggestionModel(BaseUserTest):
    """Tests for ESC Protocol suggestions"""

    def setUp(self):
        mixer.register(SpeedControllerProtocolSuggestion)
        self.protocol_suggestion = mixer.blend(SpeedControllerProtocolSuggestion)

    def test_deny(self):
        self.protocol_suggestion.deny()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 0)
        self.assertEqual(self.protocol_suggestion.status, 'denied')

    def test_accept(self):
        self.protocol_suggestion.accept()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)
        self.assertEqual(self.protocol_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.protocol_suggestion.accept()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)
        self.protocol_suggestion.delete()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.protocol_suggestion.accept()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.protocol_suggestion.accept()
        self.assertEqual(SpeedControllerProtocol.objects.count(), 1)


class TestStackSuggestionModel(BaseUserTest):
    """Tests for Stack suggestions with galleries and documents"""

    def setUp(self):

        mixer.register(FlightController,
                      description='TestFC',
                      voltage_min=2.0,
                      voltage_max=12.0,
                      mount_length=30.0,
                      mount_width=30.0,
                      weight=10.0,
                      length=35.0,
                      width=35.0)

        mixer.register(SpeedController,
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

        self.fc = mixer.blend(FlightController)
        self.esc = mixer.blend(SpeedController)

        mixer.register(StackSuggestion,
                       description='TestStack')

        self.stack_suggestion = mixer.blend(StackSuggestion,
                                            model='Test Model',
                                            manufacturer='Test Manufacturer',
                                            flight_controller=self.fc,
                                            speed_controller=self.esc)


    def test_deny(self):
        self.stack_suggestion.deny()
        self.assertEqual(Stack.objects.count(), 0)
        self.assertEqual(self.stack_suggestion.status, 'denied')

    def test_accept(self):
        self.stack_suggestion.accept()
        self.assertEqual(Stack.objects.count(), 1)
        self.assertEqual(self.stack_suggestion.status, 'approved')

    def test_accept_suggestion_with_gallery(self):
        gallery = mixer.blend(StackGallery,
                              image=self.create_image(),
                              suggestion=self.stack_suggestion)
        gallery.save()
        self.stack_suggestion.accept()
        gallery.refresh_from_db()
        self.assertEqual(self.stack_suggestion.related_instance, gallery.object)

    def test_delete_not_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(StackGallery,
                              image=self.create_image(),
                              suggestion=self.stack_suggestion)
        gallery.save()
        self.stack_suggestion.delete()
        self.assertEqual(StackGallery.objects.count(), 0)

    def test_delete_accepted_suggestion_with_gallery(self):
        gallery = mixer.blend(StackGallery,
                              image=self.create_image(),
                              suggestion=self.stack_suggestion)
        gallery.save()
        self.stack_suggestion.accept()
        self.stack_suggestion.delete()
        gallery.refresh_from_db()
        self.assertIsNone(gallery.suggestion)
        self.assertEqual(StackGallery.objects.count(), 1)
        self.assertEqual(StackSuggestion.objects.count(), 0)

    def test_accept_suggestion_with_documents(self):
        document = mixer.blend(StackDocument,
                               file=self.create_image(),
                               suggestion=self.stack_suggestion)
        document.save()
        self.stack_suggestion.accept()
        document.refresh_from_db()
        self.assertEqual(self.stack_suggestion.related_instance, document.object)

    def test_images_become_accepted_after_suggestion_accepted(self):
        gallery = mixer.blend(StackGallery,
                              image=self.create_image(),
                              suggestion=self.stack_suggestion,
                              accepted=False,
                              order=3)
        self.stack_suggestion.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.stack_suggestion.related_instance)

    def test_accept_multiple_times(self):
        self.stack_suggestion.accept()
        self.assertEqual(Stack.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.stack_suggestion.accept()
        self.assertEqual(Stack.objects.count(), 1)


class TestGyroSuggestionModel(BaseUserTest):
    """Tests for Gyro suggestions"""

    def setUp(self):
        mixer.register(GyroSuggestion,
                      description='Test Gyro',
                      max_freq=8.0)
        self.gyro_suggestion = mixer.blend(GyroSuggestion,
                                         manufacturer='Test Manufacturer',
                                         imu='Test IMU')

    def test_deny(self):
        self.gyro_suggestion.deny()
        self.assertEqual(Gyro.objects.count(), 0)
        self.assertEqual(self.gyro_suggestion.status, 'denied')

    def test_accept(self):
        self.gyro_suggestion.accept()
        self.assertEqual(Gyro.objects.count(), 1)
        self.assertEqual(self.gyro_suggestion.status, 'approved')

    def test_delete_accepted_suggestion(self):
        self.gyro_suggestion.accept()
        self.assertEqual(Gyro.objects.count(), 1)
        self.gyro_suggestion.delete()
        self.assertEqual(Gyro.objects.count(), 1)

    def test_accept_multiple_times(self):
        self.gyro_suggestion.accept()
        self.assertEqual(Gyro.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.gyro_suggestion.accept()
        self.assertEqual(Gyro.objects.count(), 1)
