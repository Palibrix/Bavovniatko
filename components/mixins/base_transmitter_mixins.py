from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class BaseTransmitterMixin(BaseComponentMixin):
    TRANSMITTER_FIELDS = [
        'manufacturer', 'model', 'description',
        'input_voltage_min', 'input_voltage_max', 'output_voltage',
        'channels_quantity', 'output', 'max_power', 'microphone',
        'length', 'height', 'thickness', 'weight'
    ]

    class OutputChoices(models.TextChoices):
        ANALOG = 'A', _('Analog')
        DIGITAL = 'D', _('Digital')

    input_voltage_min = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_('Operating Voltage Range - Min. Input Voltage'),
        verbose_name=_('Min. Input Voltage')
    )
    input_voltage_max = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_('Operating Voltage Range - Max. Input Voltage'),
        verbose_name=_('Max. Input Voltage')
    )

    output_voltage = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_('Output Voltage'),
        verbose_name=_('Output Voltage')
    )
    channels_quantity = models.PositiveIntegerField(
        help_text=_('Channels Quantity'),
        verbose_name=_('Channels Quantity')
    )

    output = models.CharField(
        max_length=10,
        choices=OutputChoices.choices,
        default=OutputChoices.ANALOG,
        verbose_name=_('Output Type'),
        help_text=_('Output Type')
    )

    max_power = models.PositiveIntegerField(
        help_text=_('Max. VTX Power'),
        verbose_name=_('Max. VTX Power')
    )

    microphone = models.BooleanField(
        default=True,
        help_text=_('Has Microphone?'),
        verbose_name=_('Built-in Microphone?')
    )

    length = models.FloatField(help_text=_('Length of the item, mm'))
    height = models.FloatField(help_text=_('Height of the item, mm'))
    thickness = models.FloatField(help_text=_('Thickness of the item, mm'))
    weight = models.FloatField(
        help_text=_('Weight oh the transmitter in grams'),
        blank=True,
        null=True
    )

    video_formats = models.ManyToManyField('components.VideoFormat')
    output_powers = models.ManyToManyField('components.OutputPower', verbose_name=_('Output Powers'))
    antenna_connectors = models.ManyToManyField('components.AntennaConnector')

    @property
    @admin.display(description=_('Input Voltage Range'))
    def get_input_voltage(self):
        return f'{self.input_voltage_min}V - {self.input_voltage_max}V'

    @property
    @admin.display(description=_('Physical Dimensions'))
    def get_dimensions(self):
        return _(f'L{self.length} x H{self.height} x T{self.thickness}')

    def clean(self):
        if not self.input_voltage_min <= self.input_voltage_max:
            raise ValidationError(_("Max. input voltage must be higher or equal to min. input voltage"))

    class Meta:
        abstract = True


class BaseOutputPowerMixin(BaseModelMixin):
    OUTPUT_POWER_FIELDS = ['output_power']

    output_power = models.PositiveIntegerField(
        verbose_name=_('Output Power'),
        unique=True
    )

    def __str__(self):
        return f'{self.output_power}mW'

    class Meta:
        abstract = True