from django.utils.translation import gettext_lazy as _

from components.mixins.base_stack_mixins import (
    BaseFlightControllerMixin,
    BaseSpeedControllerMixin,
    BaseStackMixin,
    BaseGyroMixin,
    BaseFirmwareMixin,
    BaseProtocolMixin
)


class FlightController(BaseFlightControllerMixin):

    def is_in_stack(self):
        return self.stack_set.exists()

    class Meta:
        app_label = 'components'
        db_table = 'components_fc'
        verbose_name = _('Flight Controller')
        verbose_name_plural = _('Flight Controllers')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class SpeedController(BaseSpeedControllerMixin):

    def is_in_stack(self):
        return self.stack_set.exists()

    class Meta:
        app_label = 'components'
        db_table = 'components_esc'
        verbose_name = _('Speed Controller')
        verbose_name_plural = _('Speed Controllers')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class Stack(BaseStackMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_stack'
        verbose_name = _('Stack')
        verbose_name_plural = _('Stacks')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class Gyro(BaseGyroMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_gyro'
        verbose_name = _('Gyro')
        verbose_name_plural = _('Gyros')
        ordering = ['manufacturer', 'imu']
        unique_together = ('manufacturer', 'imu', 'max_freq')


class FlightControllerFirmware(BaseFirmwareMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_fc_firmware'
        verbose_name = _('FC Firmware')
        verbose_name_plural = _('FC Firmwares')
        ordering = ['firmware']


class SpeedControllerFirmware(BaseFirmwareMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_esc_firmware'
        verbose_name = _('ESC Firmware')
        verbose_name_plural = _('ESC Firmwares')
        ordering = ['firmware']


class SpeedControllerProtocol(BaseProtocolMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_esc_protocol'
        verbose_name = _('ESC Protocol')
        verbose_name_plural = _('ESC Protocols')
        ordering = ['protocol']