from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

from components.mixins import UniqueConstraintMixin

User = get_user_model()


class Transmitter(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model',
                     'input_voltage_min', 'input_voltage_max', 'output_voltage',
                     'channels_quantity', 'output', 'max_power',
                     'microphone', 'antenna_connector', 'video_format',
                     'length', 'height', 'thickness'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'A Transmitter with these attributes already exists for this user.'

    class OutputChoices(models.TextChoices):
        ANALOG = 'A', 'Analog'
        DIGITAL = 'D', 'Digital'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")

    input_voltage_min = models.FloatField(validators=[MinValueValidator(0)],
                                          help_text=_('Operating Voltage Range - Min. Input Voltage'),
                                          verbose_name=_('Min. Input Voltage'))
    input_voltage_max = models.FloatField(validators=[MinValueValidator(0)],
                                          help_text=_('Operating Voltage Range - Max. Input Voltage'),
                                          verbose_name=_('Max. Input Voltage'))

    output_voltage = models.FloatField(validators=[MinValueValidator(0)],
                                       help_text=_('Output Voltage'),
                                       verbose_name=_('Output Voltage'))
    channels_quantity = models.IntegerField(validators=[MinValueValidator(0)],
                                            help_text=_('Channels Quantity'),
                                            verbose_name=_('Channels Quantity'))

    output = models.CharField(max_length=10, choices=OutputChoices.choices, default=OutputChoices.ANALOG,
                              verbose_name=_('Output Type'), help_text=_('Output Type'))

    max_power = models.PositiveIntegerField(help_text=_('Max. VTX Power'), verbose_name=_('Max. VTX Power'))

    microphone = models.BooleanField(default=True,
                                     help_text=_('Has Microphone?'), verbose_name=_('Built-in Microphone?'))

    antenna_connector = models.ManyToManyField('AntennaConnector')
    video_format = models.ManyToManyField('VideoFormat')

    length = models.FloatField(help_text=_('Length of the item, mm'))
    height = models.FloatField(help_text=_('Height of the item, mm'))
    thickness = models.FloatField(help_text=_('Thickness of the item, mm'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    @admin.display(description=_('Input Voltage Range'))
    def get_input_voltage(self):
        return f'{self.input_voltage_min}V - {self.input_voltage_max}V'

    @admin.display(description=_('Physical Params'))
    def get_params(self):
        return _(f'L{self.length} x H{self.height} x T{self.thickness}')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_transmitter'

        verbose_name = 'Transmitter'
        verbose_name_plural = 'Transmitters'
        ordering = ['manufacturer', 'model']


# This model is not required
class TransmitterDetail(models.Model):
    transmitter = models.ForeignKey('Transmitter', on_delete=models.CASCADE, related_name='transmitter_details')

    telemetry_power = models.FloatField(validators=[MinValueValidator(0), ], help_text=_("Telemetry Power, In dBm"))
    output_power = models.FloatField(validators=[MinValueValidator(0), ], help_text=_("Output Power, In mW"))

    def __str__(self):
        return f'{self.telemetry_power}dBm - {self.output_power}mW'

    class Meta:
        app_label = 'components'
        db_table = 'components_transmitter_details'

        verbose_name = 'Transmitter Detail'
        verbose_name_plural = 'Transmitter Details'
