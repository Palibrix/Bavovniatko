from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from components.mixins import UniqueConstraintMixin
from components.validators import validate_integer_length

User = get_user_model()


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
    tvl = models.IntegerField(validators=[MinValueValidator(500), MaxValueValidator(3000)], default=1200,
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

    def clean(self):
        if self.voltage_max < self.voltage_min:
            raise ValidationError("Max voltage must be higher or equal to min voltage")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_camera'

        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        ordering = ['manufacturer', 'model']


class CameraDetail(models.Model):
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE, related_name="camera_details")

    height = models.FloatField(max_length=5, help_text="Height of the camera in mm",
                               verbose_name="Camera mount size height")
    width = models.FloatField(max_length=5, help_text="Width of the camera in mm",
                              verbose_name="Camera mount size width")

    def __str__(self):
        return f'{self.height}x{self.width}'

    def delete(self, *args, **kwargs):
        if self.camera.camera_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only CameraDetail for this Camera.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_camera_detail'

        verbose_name = 'Camera Detail'
        verbose_name_plural = 'Camera Details'
        unique_together = ['camera', 'height', 'width']
