from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.validators import validate_fov_length


class Camera(BaseComponentMixin):

    class RatioChoices(models.TextChoices):
        NORMAL = '4:3', '4:3'
        WIDE = '16:9', '16:9'
        ANOTHER = 'another', _('Another')
        SWITCHABLE = 'switch', _('Switchable')

    class OutputChoices(models.TextChoices):
        ANALOG = 'A', _('Analog')
        DIGITAL = 'D', _('Digital')

    class SensitivityChoices(models.TextChoices):
        UNKNOWN = 'unknown', _('Unknown')
        LOW = 'low', _('Low (0.01 and higher)')
        NORMAL = 'normal', _('Normal')
        HIGH = 'high', _('High (0.00001 and below)')

    tvl = models.IntegerField(validators=[MinValueValidator(500), MaxValueValidator(3000)], default=1200,
                              help_text=_('TVL, or TV Lines - Resolution'), verbose_name=_('TVL'))

    voltage_min = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text=_('Voltage Range - Minimal Voltage'), verbose_name=_('Minimal Voltage'))
    voltage_max = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text=_('Voltage Range - Maximal Voltage'), verbose_name=_('Maximal Voltage'))

    ratio = models.CharField(max_length=10, choices=RatioChoices.choices, verbose_name=_('Aspect Ratio'),
                             help_text=_('Aspect Ratio'), default=RatioChoices.SWITCHABLE)
    fov = models.IntegerField(validators=[validate_fov_length],
                              verbose_name=_('FOV'), help_text=_('FOV Horizontally'))
    output_type = models.CharField(max_length=10, choices=OutputChoices.choices, verbose_name=_('Output Type'),
                                   default=OutputChoices.ANALOG)

    video_formats = models.ManyToManyField('VideoFormat')

    light_sens = models.CharField(max_length=10, choices=SensitivityChoices.choices, verbose_name=_('Light Sensitivity'),
                                  help_text=_('Higher light sensitivity = Better night vision'),
                                  default=SensitivityChoices.UNKNOWN)

    weight = models.FloatField(help_text=_('Weight oh the camera in grams'),
                               blank=True, null=True)

    @property
    @admin.display(description=_('Voltage'))
    def get_voltage(self):
        return f'{self.voltage_min}-{self.voltage_max}'

    def clean(self):
        if self.voltage_max < self.voltage_min:
            raise ValidationError(_("Max voltage must be higher or equal to min voltage"))

    class Meta:
        app_label = 'components'
        db_table = 'components_camera'

        verbose_name = _('Camera')
        verbose_name_plural = _('Cameras')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class CameraDetail(BaseModelMixin):
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE, related_name="details")

    height = models.FloatField(max_length=5, help_text=_("Height of the camera in mm"),
                               verbose_name=_("Camera mount size height"))
    width = models.FloatField(max_length=5, help_text=_("Width of the camera in mm"),
                              verbose_name=_("Camera mount size width"))

    def __str__(self):
        return f'{self.height}x{self.width}'

    @property
    @admin.display(description=_('Dimensions'))
    def get_dimensions(self):
        return f'{self.height}x{self.width}'

    def delete(self, *args, **kwargs):
        if self.camera.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only CameraDetail for this Camera."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_camera_detail'

        verbose_name = _('Camera Detail')
        verbose_name_plural = _('Camera Details')
        unique_together = ['camera', 'height', 'width']


class VideoFormat(BaseModelMixin):
    format = models.CharField(max_length=50, unique=True,
                              help_text=_("Format of the video (e.g. NTSC/PAL)"), verbose_name=_("Video Format"))

    def __str__(self):
        return self.format

    class Meta:
        app_label = 'components'
        db_table = 'components_video_format'

        verbose_name = _('Video Format')
        verbose_name_plural = _('Video Formats')
