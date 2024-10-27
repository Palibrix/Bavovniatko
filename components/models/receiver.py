from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class Receiver(BaseComponentMixin):

    processor = models.CharField(max_length=100, help_text=_("Name of the processor(MCU)"),
                                 null=True, blank=True)
    voltage_min = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text=_('Voltage Range - Minimal Voltage'), verbose_name=_('Minimal Voltage'))
    voltage_max = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                    help_text=_('Voltage Range - Maximal Voltage, optional'), verbose_name=_('Maximal Voltage'),
                                    null=True, blank=True)

    antenna_connectors = models.ManyToManyField('AntennaConnector')
    protocols = models.ManyToManyField('ReceiverProtocolType',
                                      verbose_name=_("Output Protocol"), help_text=_("Rx To FC"))

    @property
    # @admin.display(_('Voltage'))
    def get_voltage(self):
        if not self.voltage_max:
            return f'{self.voltage_min}V'
        else:
            return f'{self.voltage_min}-{self.voltage_max}V'

    def clean(self):
        if not self.voltage_min <= self.voltage_max:
            raise ValidationError(_("Max voltage must be higher or equal to min voltage."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver'

        verbose_name = _('Receiver')
        verbose_name_plural = _('Receivers')
        ordering = ['manufacturer', 'model', ]


class ReceiverDetail(BaseModelMixin):
    receiver = models.ForeignKey('Receiver', on_delete=models.PROTECT, related_name='details')

    frequency = models.FloatField(validators=[MinValueValidator(0), ], help_text=_('Frequency, in Mhz'),
                                  verbose_name=_('Frequency'))
    weight = models.FloatField(validators=[MinValueValidator(0), ], help_text=_('Weight in grams, without Antenna'))
    telemetry_power = models.FloatField(validators=[MinValueValidator(0), ], help_text=_("Telemetry Power, In dBm"))
    rf_chip = models.CharField(max_length=50, help_text=_("RF Chip Number"),
                               null=True, blank=True)

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.receiver.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only ReceiverDetail for this Receiver.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_detail'

        verbose_name = _('Receiver Detail')
        verbose_name_plural = _('Receiver Details')
        ordering = ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip']
        unique_together = ['receiver', 'frequency']


class ReceiverProtocolType(BaseModelMixin):
    type = models.CharField(max_length=50, verbose_name="Output Protocol Type", help_text="Rx To FC")

    def __str__(self):
        return self.type

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_protocol_type'

        verbose_name = _('Receiver Protocol Type')
        verbose_name_plural = _('Receiver Protocol Types')
        ordering = ['type',]
