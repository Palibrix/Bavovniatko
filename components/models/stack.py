from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import UniqueConstraintMixin

User = get_user_model()


class FlightController(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model',
                     'gyro', 'osd', 'bluetooth', 'wifi', 'barometer',
                     'voltage', 'connector_type',
                     ]
    fields_private = fields_public + ['user', ]
    error_message = _('A FC with these attributes already exists for this user.')

    class ConnectorTypeChoices(models.TextChoices):
        MICRO = 'micro', _('Micro-USB')
        C = 'c', _('Type C')
        Another = 'another', _('Another')

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text=_("Full name of the item"))
    microcontroller = models.CharField(max_length=50, help_text=_("Microcontroller Unit"),
                                       verbose_name=_("Microcontroller Unit"))
    gyro = models.ForeignKey('Gyro', on_delete=models.CASCADE)
    osd = models.CharField(max_length=50, help_text=_("OSD Chip Model"), verbose_name=_("OSD Chip"))

    bluetooth = models.BooleanField(help_text=_("Bluetooth Support"), default=True)
    wifi = models.BooleanField(help_text=_("Wifi Support"), default=True)
    barometer = models.BooleanField(help_text=_("Barometer Support"), default=True)

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_("Public if empty"),
                             blank=True, null=True)

    @property
    @admin.display(description='Physical Params')
    def get_params(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
        else:
            return _(f'L{self.length} x W{self.width}')

    @property
    @admin.display(description='Mount Params')
    def get_mount_params(self):
        return _(f'L{self.mount_length} x W{self.mount_width}')

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.get_mount_params}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_fc'

        verbose_name = _('Flight Controller')
        verbose_name_plural = _('Flight Controllers')
        ordering = ('manufacturer', 'model')


class SpeedController(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model',
                     'voltage', 'esc_type', 'cont_current', 'burst_current',
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A ESC with these attributes already exists for this user.'

    class ESCTypeChoices(models.TextChoices):
        ALL = 'all', _('4-in-1')
        SINGLE = 'single', _('Single')

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")

    voltage = models.ForeignKey('RatedVoltage', on_delete=models.CASCADE, related_name='esc_power_input',
                                verbose_name=_('Power Input'))
    is_wireless_conf = models.BooleanField(default=True, verbose_name=_('Is Wireless Configuration Available?'))
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_("Public if empty"),
                             blank=True, null=True)

    @property
    @admin.display(description='Physical Params')
    def get_params(self):
        if self.height:
            return _(f'L{self.length} x H{self.height} x W{self.width}')
        else:
            return _(f'L{self.length} x W{self.width}')

    @property
    @admin.display(description='Mount Params')
    def get_mount_params(self):
        return _(f'L{self.mount_length} x W{self.mount_width}')

    @property
    @admin.display(description='Cont. Current, A')
    def get_cont_current(self):
        return f'{self.cont_current}A'

    @property
    @admin.display(description='Burst Current, A')
    def get_burst_current(self):
        return f'{self.burst_current}A'

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.get_cont_current} {self.get_mount_params} {self.esc_type}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_esc'

        verbose_name = _('Speed Controller')
        verbose_name_plural = _('Speed Controllers')
        ordering = ('manufacturer', 'model')


class Stack(models.Model, UniqueConstraintMixin):
    fields_public = ['model',
                     'flight_controller', 'speed_controller'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Stack with these attributes already exists for this user.'

    model = models.CharField(max_length=50, help_text="Full name of the item")
    flight_controller = models.ForeignKey('FlightController', on_delete=models.CASCADE)
    speed_controller = models.ForeignKey('SpeedController', on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_("Public if empty"),
                             blank=True, null=True)

    def __str__(self):
        return f'{self.model}'

    class Meta:
        app_label = 'components'
        db_table = 'components_stack'

        verbose_name = _('Stack')
        verbose_name_plural = _('Stacks')
        ordering = ('model',)


class Gyro(models.Model):
    manufacturer = models.CharField(max_length=50)
    imu = models.CharField(max_length=50, help_text=_("Inertial Measurement Unit (e.g. MPU6000, BMI270)"),
                           verbose_name=_("Inertial Measurement Unit"))
    max_freq = models.FloatField(max_length=50, verbose_name=_("Maximum Frequency"),
                                 help_text=_("Max. Effective Gyro Sampling Frequency, KHz"))
    spi_support = models.BooleanField(default=True, verbose_name=_("SPI Support"))

    def __str__(self):
        return f'{self.imu} {self.manufacturer} {self.get_max_freq}'

    @property
    @admin.display(description='Max. Frequency')
    def get_max_freq(self):
        return f'{self.max_freq}KHz'

    class Meta:
        app_label = 'components'
        db_table = 'components_gyro'

        verbose_name = 'Gyro'
        verbose_name_plural = 'Gyros'
        unique_together = ('manufacturer', 'imu', 'max_freq', 'spi_support')


class FlightControllerFirmware(models.Model):
    firmware = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. BetaFlight, OneShot125)"), unique=True)

    def __str__(self):
        return self.firmware

    class Meta:
        app_label = 'components'
        db_table = 'components_fc_firmware'
        verbose_name = 'FC Firmware'
        verbose_name_plural = 'FC Firmwares'


class SpeedControllerFirmware(models.Model):
    firmware = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. BLHeli_S, AM32)"), unique=True)

    def __str__(self):
        return self.firmware

    class Meta:
        app_label = 'components'
        db_table = 'components_esc_firmware'

        verbose_name = 'ESC Firmware'
        verbose_name_plural = 'ESC Firmwares'


class SpeedControllerProtocol(models.Model):
    protocol = models.CharField(max_length=50, help_text=_("Firmware Type (e.g. DShot150 , DShot300 )"), unique=True)

    def __str__(self):
        return self.protocol

    class Meta:
        app_label = 'components'
        db_table = 'components_esc_protocol'

        verbose_name = 'ESC Protocol'
        verbose_name_plural = 'ESC Protocols'
