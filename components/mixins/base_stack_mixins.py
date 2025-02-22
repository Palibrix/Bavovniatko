from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class BaseFlightControllerMixin(BaseComponentMixin):
    FC_FIELDS = [
        'manufacturer', 'model', 'description',
        'microcontroller', 'gyro', 'osd',
        'bluetooth', 'wifi', 'barometer',
        'voltage', 'connector_type',
        'mount_length', 'mount_width', 'weight',
        'length', 'height', 'width',
        'firmwares'
    ]

    class ConnectorTypeChoices(models.TextChoices):
        MICRO = 'micro', _('Micro-USB')
        C = 'c', _('Type C')
        Another = 'another', _('Another')

    microcontroller = models.CharField(max_length=50,
                                       help_text=_("Microcontroller Unit"),
                                       verbose_name=_("Microcontroller Unit"))
    gyro = models.ForeignKey('components.Gyro', on_delete=models.CASCADE)
    osd = models.CharField(max_length=50,
                           help_text=_("OSD Chip Model"),
                           verbose_name=_("OSD Chip"),
                           null=True, blank=True)

    bluetooth = models.BooleanField(help_text=_("Bluetooth Support"), default=False)
    wifi = models.BooleanField(help_text=_("Wifi Support"), default=False)
    barometer = models.BooleanField(help_text=_("Barometer Support"), default=False)

    voltage = models.ForeignKey('components.RatedVoltage',
                                on_delete=models.CASCADE,
                                related_name='%(class)s_power_input',
                                verbose_name=_('Power Input'))
    firmwares = models.ManyToManyField('components.FlightControllerFirmware',
                                       verbose_name=_("Supported Firmwares"),
                                       help_text=_("Compatible firmware types"))

    connector_type = models.CharField(max_length=50,
                                      choices=ConnectorTypeChoices.choices,
                                      verbose_name=_("Connector Type"))

    mount_length = models.FloatField(help_text=_("Length of the FC in mm"),
                                     verbose_name=_("FC mount Length, mm"))
    mount_width = models.FloatField(help_text=_("Width of the FC in mm"),
                                    verbose_name=_("FC mount width, mm"))
    weight = models.FloatField(validators=[MinValueValidator(0)],
                               help_text=_("FC weight in grams"))

    length = models.FloatField(help_text=_('Length of the FC, mm'))
    height = models.FloatField(help_text=_('Height of the FC, mm'),
                               null=True, blank=True)
    width = models.FloatField(help_text=_('Width of the FC, mm'))

    @property
    @admin.display(description=_('Physical Dimensions'))
    def get_dimensions(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
        return _(f'L{self.length} x W{self.width}')

    @property
    @admin.display(description=_('Mount Dimensions'))
    def get_mount_dimensions(self):
        return _(f'L{self.mount_length} x W{self.mount_width}')

    class Meta:
        abstract = True


class BaseSpeedControllerMixin(BaseComponentMixin):
    ESC_FIELDS = [
        'manufacturer', 'model', 'description',
        'voltage', 'is_wireless_conf', 'esc_type',
        'cont_current', 'burst_current',
        'mount_length', 'mount_width', 'weight',
        'length', 'height', 'width',
        'firmwares', 'protocols'
    ]

    class ESCTypeChoices(models.TextChoices):
        ALL = 'all', _('4-in-1')
        SINGLE = 'single', _('Single')

    voltage = models.ForeignKey('components.RatedVoltage',
                                on_delete=models.CASCADE,
                                related_name='%(class)s_power_input',
                                verbose_name=_('Power Input'))

    is_wireless_conf = models.BooleanField(default=False,
                                           verbose_name=_('Is Wireless Configuration Available?'))
    esc_type = models.CharField(max_length=50, choices=ESCTypeChoices.choices)
    cont_current = models.FloatField(validators=[MinValueValidator(0)],
                                     help_text=_("Continuous current, A"))
    burst_current = models.FloatField(validators=[MinValueValidator(0)],
                                      help_text=_("Burst current, A"))

    mount_length = models.FloatField(help_text=_("Length of the ESC in mm"),
                                     verbose_name=_("ESC mount Length, mm"))
    mount_width = models.FloatField(help_text=_("Width of the ESC in mm"),
                                    verbose_name=_("ESC mount width, mm"))
    weight = models.FloatField(validators=[MinValueValidator(0)],
                               help_text=_("ESC weight in grams"))

    length = models.FloatField(help_text=_('Length of the ESC, mm'))
    height = models.FloatField(help_text=_('Height of the ESC, mm'),
                               null=True, blank=True)
    width = models.FloatField(help_text=_('Width of the ESC, mm'))

    firmwares = models.ManyToManyField('components.SpeedControllerFirmware',
                                       verbose_name=_("Supported Firmwares"),
                                       help_text=_("Compatible firmware types"))

    protocols = models.ManyToManyField('components.SpeedControllerProtocol',
                                       verbose_name=_("Supported Protocols"),
                                       help_text=_("Compatible communication protocols"))

    @property
    @admin.display(description=_('Physical Dimensions'))
    def get_dimensions(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
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

    class Meta:
        abstract = True


class BaseStackMixin(BaseComponentMixin):
    STACK_FIELDS = [
        'manufacturer', 'model', 'description',
        'flight_controller', 'speed_controller'
    ]

    flight_controller = models.ForeignKey('components.FlightController',
                                          on_delete=models.CASCADE)
    speed_controller = models.ForeignKey('components.SpeedController',
                                         on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseGyroMixin(BaseModelMixin):
    GYRO_FIELDS = ['manufacturer', 'imu', 'max_freq', 'spi_support']

    manufacturer = models.CharField(max_length=50)
    imu = models.CharField(max_length=50,
                           help_text=_("Inertial Measurement Unit (e.g. MPU6000, BMI270)"),
                           verbose_name=_("Inertial Measurement Unit"))
    max_freq = models.FloatField(verbose_name=_("Maximum Frequency"),
                                 help_text=_("Max. Effective Gyro Sampling Frequency, KHz"))
    spi_support = models.BooleanField(default=False,
                                      verbose_name=_("SPI Support"))

    @property
    @admin.display(description='Max. Frequency')
    def get_max_freq(self):
        return f'{self.max_freq}KHz'

    class Meta:
        abstract = True


class BaseFirmwareMixin(BaseModelMixin):
    FIRMWARE_FIELDS = ['firmware']

    firmware = models.CharField(max_length=50,
                                help_text=_("Firmware Type"),
                                unique=True)

    def __str__(self):
        return self.firmware

    class Meta:
        abstract = True


class BaseProtocolMixin(BaseModelMixin):
    PROTOCOL_FIELDS = ['protocol']

    protocol = models.CharField(max_length=50,
                                help_text=_("Protocol Type"),
                                unique=True)

    def __str__(self):
        return self.protocol

    class Meta:
        abstract = True