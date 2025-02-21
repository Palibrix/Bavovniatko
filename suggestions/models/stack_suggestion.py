from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_stack_mixins import (
    BaseFlightControllerMixin,
    BaseSpeedControllerMixin,
    BaseStackMixin,
    BaseGyroMixin,
    BaseFirmwareMixin,
    BaseProtocolMixin
)
from components.models import (
    FlightController,
    SpeedController,
    Stack,
    Gyro,
    FlightControllerFirmware,
    SpeedControllerFirmware,
    SpeedControllerProtocol
)
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin, MediaHandlerMixin


class FlightControllerSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseFlightControllerMixin,
                                 BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.FlightController', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)

    def _create_instance(self):
        instance = FlightController.objects.create(
            **{field: getattr(self, field)
               for field in self.FC_FIELDS
               if field != 'firmwares' and hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        if hasattr(self, 'firmwares') and self.firmwares.exists():
            instance.firmwares.set(self.firmwares.all())

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_flight_controller'
        verbose_name = _('Flight Controller Suggestion')
        verbose_name_plural = _('Flight Controller Suggestions')
        ordering = ['manufacturer', 'model']


class SpeedControllerSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseSpeedControllerMixin,
                                BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.SpeedController', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)

    def _create_instance(self):
        instance = SpeedController.objects.create(
            **{field: getattr(self, field)
               for field in self.ESC_FIELDS
               if field not in ['firmwares', 'protocols'] and hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        if hasattr(self, 'firmwares') and self.firmwares.exists():
            instance.firmwares.set(self.firmwares.all())

        if hasattr(self, 'protocols') and self.protocols.exists():
            instance.protocols.set(self.protocols.all())

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_speed_controller'
        verbose_name = _('Speed Controller Suggestion')
        verbose_name_plural = _('Speed Controller Suggestions')
        ordering = ['manufacturer', 'model']


class StackSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseStackMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Stack', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)

    def _create_instance(self):
        instance = Stack.objects.create(
            **{field: getattr(self, field)
               for field in self.STACK_FIELDS
               if hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_stack'
        verbose_name = _('Stack Suggestion')
        verbose_name_plural = _('Stack Suggestions')
        ordering = ['manufacturer', 'model']


class GyroSuggestion(BaseGyroMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Gyro', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = Gyro.objects.create(
            **{field: getattr(self, field)
               for field in self.GYRO_FIELDS
               if hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_gyro'
        verbose_name = _('Gyro Suggestion')
        verbose_name_plural = _('Gyro Suggestions')
        ordering = ['manufacturer', 'imu']


class FlightControllerFirmwareSuggestion(BaseFirmwareMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.FlightControllerFirmware', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = FlightControllerFirmware.objects.create(
            **{field: getattr(self, field)
               for field in self.FIRMWARE_FIELDS
               if hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_fc_firmware'
        verbose_name = _('FC Firmware Suggestion')
        verbose_name_plural = _('FC Firmware Suggestions')
        ordering = ['firmware']


class SpeedControllerFirmwareSuggestion(BaseFirmwareMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.SpeedControllerFirmware', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = SpeedControllerFirmware.objects.create(
            **{field: getattr(self, field)
               for field in self.FIRMWARE_FIELDS
               if hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_esc_firmware'
        verbose_name = _('ESC Firmware Suggestion')
        verbose_name_plural = _('ESC Firmware Suggestions')
        ordering = ['firmware']


class SpeedControllerProtocolSuggestion(BaseProtocolMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.SpeedControllerProtocol', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = SpeedControllerProtocol.objects.create(
            **{field: getattr(self, field)
               for field in self.PROTOCOL_FIELDS
               if hasattr(self, field)}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_esc_protocol'
        verbose_name = _('ESC Protocol Suggestion')
        verbose_name_plural = _('ESC Protocol Suggestions')
        ordering = ['protocol']