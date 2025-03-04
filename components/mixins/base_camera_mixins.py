from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.validators import validate_fov_length
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseCameraMixin(BaseComponentMixin):
    CAMERA_FIELDS = [
        'manufacturer', 'model', 'description',
        'tvl', 'voltage_min', 'voltage_max', 'ratio',
        'fov', 'output_type', 'light_sens', 'weight'
    ]

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

    video_formats = models.ManyToManyField('components.VideoFormat')

    light_sens = models.CharField(max_length=10, choices=SensitivityChoices.choices,
                                  verbose_name=_('Light Sensitivity'),
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
        abstract = True

class BaseCameraDetailMixin(BaseModelMixin):
    DETAIL_FIELDS = ['height', 'width']

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


    class Meta:
        abstract = True

class BaseVideoFormatMixin(BaseModelMixin):
    VIDEO_FORMAT_FIELDS = ['format']

    format = models.CharField(max_length=50, unique=True,
                              help_text=_("Format of the video (e.g. NTSC/PAL)"), verbose_name=_("Video Format"))

    def __str__(self):
        return self.format

    class Meta:
        abstract = True