from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from components.mixins import UniqueConstraintMixin
from components.validators import validate_integer_length, validate_even_number

User = get_user_model()


# class Motor(models.Model):
#     raise NotImplementedError
#
#
# class Transmitter(models.Model):
#     raise NotImplementedError
#
#
class Receiver(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model', 'processor', 'voltage_min', 'voltage_max'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Frame with these attributes already exists for this user.'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")

    processor = models.CharField(max_length=100, help_text="Name of the processor",
                                 null=True, blank=True)
    voltage_min = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text='Voltage Range - Minimal Voltage', verbose_name='Minimal Voltage')
    voltage_max = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text='Voltage Range - Maximal Voltage', verbose_name='Maximal Voltage',
                                    null=True, blank=True)

    antenna_connector = models.ManyToManyField('AntennaConnector')
    protocol = models.ManyToManyField('ReceiverProtocol',
                                      verbose_name="Output Protocol", help_text="Rx To FC")

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Receiver'
        verbose_name_plural = 'Receivers'
        ordering = ['manufacturer', 'model',]


class Camera(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model',
                     'tvl', 'voltage_min', 'voltage_max', 'ratio', 'fov',
                     'output_type', 'light_sens',
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Camera with these attributes already exists for this user.'

    class RatioChoices(models.TextChoices):
        NORMAL = '4:3', '4:3'
        WIDE = '16:9', '16:9'
        SWITCHABLE = 'switch', 'Switchable'

    class OutputChoices(models.TextChoices):
        ANALOG = 'A', 'Analog'
        DIGITAL = 'D', 'Digital'

    class SensitivityChoices(models.TextChoices):
        UNKNOWN = 'unknown', 'Unknown'
        LOW = 'low', 'Low (0.01 and higher)'
        NORMAL = 'normal', 'Normal'
        HIGH = 'high', 'High (0.00001 and below)'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")
    tvl = models.IntegerField(validators=[MinValueValidator(500), MaxValueValidator(1800)], default=1200,
                              help_text='TVL, or TV Lines - Resolution', verbose_name='TVL')
    voltage_min = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text='Voltage Range - Minimal Voltage', verbose_name='Minimal Voltage')
    voltage_max = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text='Voltage Range - Maximal Voltage', verbose_name='Maximal Voltage')
    ratio = models.CharField(max_length=10, choices=RatioChoices.choices, verbose_name='Aspect Ratio',
                             help_text='Aspect Ratio', default=RatioChoices.SWITCHABLE)
    fov = models.IntegerField(validators=[validate_integer_length],
                              verbose_name='FOV', help_text='FOV Horizontally')
    output_type = models.CharField(max_length=10, choices=OutputChoices.choices, verbose_name='Output Type',
                                   default=OutputChoices.ANALOG)
    light_sens = models.CharField(max_length=10, choices=SensitivityChoices.choices, verbose_name='Light Sensitivity',
                                  help_text='Higher light sensitivity = Better night vision',
                                  default=SensitivityChoices.UNKNOWN)

    weight = models.FloatField(help_text='Weight oh the camera in grams',
                               blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.voltage_max < self.voltage_min:
            raise ValidationError("Max voltage must be higher or equal to min voltage")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        ordering = ['manufacturer', 'model']


class Propeller(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model', 'size', 'pitch', 'blade_count', 'weight']
    fields_private = ['manufacturer', 'model', 'size', 'pitch', 'blade_count', 'user']
    error_message = 'A Propeller with these attributes already exists for this user.'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")
    size = models.FloatField(validators=[MinValueValidator(2)],
                             help_text="Size of the propeller in inches")
    pitch = models.FloatField(help_text="Pitch of the propeller in inches")
    blade_count = models.CharField(max_length=10,
                                   choices=[(str(i), str(i)) for i in range(2, 11)] + [('another', 'Another')], )
    weight = models.FloatField(help_text="Weight of propeller in grams",
                               blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Propeller'
        verbose_name_plural = 'Propellers'
        ordering = ['model', ]


class Frame(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model', 'prop_size', 'size',
                     'weight', 'material', 'configuration'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Frame with these attributes already exists for this user.'

    class MaterialChoice(models.TextChoices):
        ALUMINIUM = 'aluminum', 'Aluminium'
        FIBRE = 'fibre', 'Carbon fibre'

    class ConfigurationChoice(models.TextChoices):
        H_FRAME = 'h', 'H Frame'
        X = 'x', 'X Frame'
        HYBRID = 'hybrid', 'Hybrid-X'
        BOX = 'box', 'Box'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")
    prop_size = models.CharField(max_length=50, help_text="Propeller size in inches",
                                 verbose_name="Propeller size")
    size = models.CharField(max_length=50, help_text="Size(Diagonal) of the frame in mm",
                            verbose_name="Frame size")

    weight = models.FloatField(help_text='Weight oh the frame in grams',
                               blank=True, null=True)
    material = models.CharField(max_length=50, choices=MaterialChoice.choices,
                                blank=True, null=True)
    configuration = models.CharField(max_length=50, choices=ConfigurationChoice.choices,
                                     blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        # self.frame_detail.count()
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Frame'
        verbose_name_plural = 'Frames'
        ordering = ['manufacturer', 'model', ]


# class Stack(models.Model):
#     raise NotImplementedError

# class Antenna(models.Model, UniqueConstraintMixin):
#     raise NotImplementedError

class ReceiverDetail(models.Model):
    receiver = models.ForeignKey('Receiver', on_delete=models.PROTECT, related_name='receiver_details')

    frequency = models.FloatField(validators=[MinValueValidator(0), ], )
    weight = models.FloatField(validators=[MinValueValidator(0), ], )
    telemetry_power = models.FloatField(validators=[MinValueValidator(0), ], help_text="Telemetry Power, In dBm")
    rf_chip = models.CharField(max_length=50, help_text="RF Chip Number",
                               null=True, blank=True)

    def __str__(self):
        return f"{self.frequency}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Receiver Detail'
        verbose_name_plural = 'Receiver Details'
        ordering = ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip']
        unique_together = ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip']


class ReceiverProtocol(models.Model):
    type = models.CharField(max_length=50, verbose_name="Output Protocol Type", help_text="Rx To FC")
    is_custom = models.BooleanField(default=True, help_text="Created by user?")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Receiver Protocol'
        verbose_name_plural = 'Receiver Protocols'
        ordering = ['type', '-is_custom']


class AntennaConnector(models.Model):
    type = models.CharField(max_length=50, help_text="Type of antenna connector")
    is_custom = models.BooleanField(default=True, help_text="Created by user?")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Antenna Connector'
        verbose_name_plural = 'Antenna Connectors'
        ordering = ['type', '-is_custom']


class CameraDetail(models.Model):
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)

    height = models.FloatField(max_length=5, help_text="Height of the camera in mm",
                               verbose_name="Camera mount size height")
    width = models.FloatField(max_length=5, help_text="Width of the camera in mm",
                              verbose_name="Camera mount size width")

    def __str__(self):
        return f'{self.height}x{self.width}'

    class Meta:
        verbose_name = 'Camera Detail'
        verbose_name_plural = 'Camera Details'
        unique_together = ['camera', 'height', 'width']


class FrameDetail(models.Model):
    frame = models.ForeignKey('Frame', on_delete=models.CASCADE, related_name='frame_details')

    camera_mount_height = models.FloatField(max_length=5, help_text="Height of the camera in mm",
                                            verbose_name="Camera mount size height")
    camera_mount_width = models.FloatField(max_length=5, help_text="Width of the camera in mm",
                                           verbose_name="Camera mount size width")

    motor_mount_height = models.FloatField(max_length=5, help_text="Height of the motor in mm",
                                           verbose_name="Motor mount size height")
    motor_mount_width = models.FloatField(max_length=5, help_text="Width of the motor in mm",
                                          verbose_name="Motor mount size width")

    vtx_mount_height = models.FloatField(max_length=5, help_text="Height of the vtx in mm",
                                         verbose_name="VTX mount size height")
    vtx_mount_width = models.FloatField(max_length=5, help_text="Width of the vtx in mm",
                                        verbose_name="VTX mount size width")

    def __str__(self):
        return self.frame.model

    def delete(self, *args, **kwargs):
        if self.frame.frame_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only FrameDetail for this Frame.", self)

    class Meta:
        verbose_name = 'FrameDetail'
        verbose_name_plural = 'FrameDetails'
        ordering = ('frame__manufacturer', 'frame__model')
        unique_together = ['frame', 'camera_mount_height', 'camera_mount_width',
                           'motor_mount_height', 'motor_mount_width',
                           'vtx_mount_height', 'vtx_mount_width']
