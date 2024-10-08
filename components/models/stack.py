from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class FlightController(BaseComponentMixin):

    class ConnectorTypeChoices(models.TextChoices):
        MICRO = 'micro', _('Micro-USB')
        C = 'c', _('Type C')
        Another = 'another', _('Another')

    microcontroller = models.CharField(max_length=50, help_text=_("Microcontroller Unit"),
                                       verbose_name=_("Microcontroller Unit"))
    gyro = models.ForeignKey('Gyro', on_delete=models.CASCADE)
    osd = models.CharField(max_length=50, help_text=_("OSD Chip Model"), verbose_name=_("OSD Chip"),
                           null=True, blank=True)

    bluetooth = models.BooleanField(help_text=_("Bluetooth Support"), default=False)
    wifi = models.BooleanField(help_text=_("Wifi Support"), default=False)
    barometer = models.BooleanField(help_text=_("Barometer Support"), default=False)

    voltage = models.ForeignKey('RatedVoltage', on_delete=models.CASCADE, related_name='fc_power_input',
                                verbose_name=_('Power Input'))
    firmwares = models.ManyToManyField('FlightControllerFirmware')

    connector_type = models.CharField(max_length=50, choices=ConnectorTypeChoices.choices,
                                      verbose_name=_("Connector Type"))

    mount_length = models.FloatField(max_length=5, help_text=_("Length of the FC in mm"),
                                     verbose_name=_("FC mount Length, mm"))
    mount_width = models.FloatField(max_length=5, help_text=_("Width of the FC in mm"),
                                    verbose_name=_("FC mount width, mm"))
    weight = models.FloatField(validators=[MinValueValidator(0),], help_text=_("FC weight in grams"))

    length = models.FloatField(help_text=_('Length of the FC, mm'))
    height = models.FloatField(help_text=_('Height of the FC, mm'),
                               null=True, blank=True)
    width = models.FloatField(help_text=_('Width of the FC, mm'))

    @property
    @admin.display(description=_('Physical Dimensions'))
    def get_dimensions(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
        else:
            return _(f'L{self.length} x W{self.width}')

    @property
    @admin.display(description=_('Mount Dimensions'))
    def get_mount_dimensions(self):
        return _(f'L{self.mount_length} x W{self.mount_width}')

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.get_mount_dimensions}'

    class Meta:
        app_label = 'components'
        db_table = 'components_fc'

        verbose_name = _('Flight Controller')
        verbose_name_plural = _('Flight Controllers')


class SpeedController(BaseComponentMixin):

    class ESCTypeChoices(models.TextChoices):
        ALL = 'all', _('4-in-1')
        SINGLE = 'single', _('Single')

    voltage = models.ForeignKey('RatedVoltage', on_delete=models.CASCADE, related_name='esc_power_input',
                                verbose_name=_('Power Input'))

    is_wireless_conf = models.BooleanField(default=False, verbose_name=_('Is Wireless Configuration Available?'))
    esc_type = models.CharField(max_length=50, choices=ESCTypeChoices.choices,)
    cont_current = models.FloatField(validators=[MinValueValidator(0),], help_text=_("Continuous current, A"))
    burst_current = models.FloatField(validators=[MinValueValidator(0),], help_text=_("Burst current, A"))

    firmwares = models.ManyToManyField('SpeedControllerFirmware')
    protocols = models.ManyToManyField('SpeedControllerProtocol')

    mount_length = models.FloatField(max_length=5, help_text=_("Length of the ESC in mm"),
                                     verbose_name=_("ESC mount Length, mm"))
    mount_width = models.FloatField(max_length=5, help_text=_("Width of the ESC in mm"),
                                    verbose_name=_("ESC mount width, mm"))
    weight = models.FloatField(validators=[MinValueValidator(0), ], help_text=_("ESC weight in grams"))

    length = models.FloatField(help_text=_('Length of the ESC, mm'))
    height = models.FloatField(help_text=_('Height of the ESC, mm'),
                               null=True, blank=True)
    width = models.FloatField(help_text=_('Width of the ESC, mm'))

    @property
    @admin.display(description=_('Physical Dimensions'))
    def get_dimensions(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
        else:
            return _(f'L{self.length} x W{self.width}')

    @property
    @admin.display(description=_('Mount Dimensions'))
    def get_mount_dimensions(self):
        return _(f'L{self.mount_length} x W{self.mount_width}')

    @property
    @admin.display(description=_('Cont. Current, A'))
    def get_cont_current(self):
        return f'{self.cont_current}A'

    @property
    @admin.display(description=_('Burst Current, A'))
    def get_burst_current(self):
        return f'{self.burst_current}A'

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.get_cont_current} {self.get_mount_dimensions} {self.esc_type}'

    class Meta:
        app_label = 'components'
        db_table = 'components_esc'

        verbose_name = _('Speed Controller')
        verbose_name_plural = _('Speed Controllers')


class Stack(BaseComponentMixin):

    flight_controller = models.ForeignKey('FlightController', on_delete=models.CASCADE)
    speed_controller = models.ForeignKey('SpeedController', on_delete=models.CASCADE)

    class Meta:
        app_label = 'components'
        db_table = 'components_stack'

        verbose_name = _('Stack')
        verbose_name_plural = _('Stacks')


class Gyro(BaseModelMixin):

    manufacturer = models.CharField(max_length=50)
    imu = models.CharField(max_length=50, help_text=_("Inertial Measurement Unit (e.g. MPU6000, BMI270)"),
                           verbose_name=_("Inertial Measurement Unit"))
    max_freq = models.FloatField(max_length=50, verbose_name=_("Maximum Frequency"),
                                 help_text=_("Max. Effective Gyro Sampling Frequency, KHz"))
    spi_support = models.BooleanField(default=False, verbose_name=_("SPI Support"))

    def __str__(self):
        return f'{self.imu} {self.manufacturer} {self.get_max_freq}'

    @property
    @admin.display(description='Max. Frequency')
    def get_max_freq(self):
        return f'{self.max_freq}KHz'

    class Meta:
        app_label = 'components'
        db_table = 'components_gyro'

        verbose_name = _('Gyro')
        verbose_name_plural = _('Gyros')
        unique_together = ('manufacturer', 'imu', 'max_freq')


class FlightControllerFirmware(BaseModelMixin):
    firmware = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. BetaFlight, OneShot125)"), unique=True)

    def __str__(self):
        return self.firmware

    class Meta:
        app_label = 'components'
        db_table = 'components_fc_firmware'
        verbose_name = _('FC Firmware')
        verbose_name_plural = _('FC Firmwares')


class SpeedControllerFirmware(BaseModelMixin):
    firmware = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. BLHeli_S, AM32)"), unique=True)

    def __str__(self):
        return self.firmware

    class Meta:
        app_label = 'components'
        db_table = 'components_esc_firmware'

        verbose_name = _('ESC Firmware')
        verbose_name_plural = _('ESC Firmwares')


class SpeedControllerProtocol(BaseModelMixin):
    protocol = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. DShot150 , DShot300 )"), unique=True)

    def __str__(self):
        return self.protocol

    class Meta:
        app_label = 'components'
        db_table = 'components_esc_protocol'

        verbose_name = _('ESC Protocol')
        verbose_name_plural = _('ESC Protocols')
