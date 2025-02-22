from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class BaseReceiverMixin(BaseComponentMixin):
    RECEIVER_FIELDS = [
        'manufacturer', 'model', 'description',
        'processor', 'voltage_min', 'voltage_max',
        'antenna_connectors', 'protocols'
    ]

    processor = models.CharField(max_length=100,
                                 help_text=_("Name of the processor(MCU)"),
                                 null=True, blank=True)

    voltage_min = models.FloatField(
        validators=[MinValueValidator(2), MaxValueValidator(28)],
        help_text=_('Voltage Range - Minimal Voltage'),
        verbose_name=_('Minimal Voltage')
    )
    voltage_max = models.FloatField(
        validators=[MinValueValidator(2), MaxValueValidator(28)],
        help_text=_('Voltage Range - Maximal Voltage, optional'),
        verbose_name=_('Maximal Voltage'),
        null=True, blank=True
    )

    antenna_connectors = models.ManyToManyField('components.AntennaConnector')
    protocols = models.ManyToManyField('components.ReceiverProtocolType',
                                       verbose_name=_("Output Protocol"),
                                       help_text=_("Rx To FC"))

    @property
    @admin.display(description=_('Voltage'))
    def get_voltage(self):
        if not self.voltage_max:
            return f'{self.voltage_min}V'
        return f'{self.voltage_min}-{self.voltage_max}V'

    def clean(self):
        if self.voltage_max and self.voltage_min > self.voltage_max:
            raise ValidationError(_("Max voltage must be higher or equal to min voltage."))

    class Meta:
        abstract = True


class BaseReceiverDetailMixin(BaseModelMixin):
    DETAIL_FIELDS = [
        'frequency', 'weight', 'telemetry_power', 'rf_chip'
    ]

    frequency = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_('Frequency, in Mhz'),
        verbose_name=_('Frequency')
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_('Weight in grams, without Antenna')
    )
    telemetry_power = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_("Telemetry Power, In dBm")
    )
    rf_chip = models.CharField(
        max_length=50,
        help_text=_("RF Chip Number"),
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.frequency}"

    @property
    @admin.display(description=_('Telemetry'))
    def get_telemetry(self):
        return f'{self.telemetry_power}dBm'

    @property
    @admin.display(description=_('Frequency'))
    def get_frequency(self):
        return f'{self.frequency}Mhz'

    class Meta:
        abstract = True


class BaseProtocolTypeMixin(BaseModelMixin):
    PROTOCOL_FIELDS = ['type']

    type = models.CharField(
        max_length=50,
        verbose_name=_("Output Protocol Type"),
        help_text=_("Rx To FC"),
        unique=True
    )

    def __str__(self):
        return self.type

    class Meta:
        abstract = True