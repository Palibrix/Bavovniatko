from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from components.mixins import UniqueConstraintMixin

User = get_user_model()


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
    protocol = models.ManyToManyField('ReceiverProtocolType',
                                      verbose_name="Output Protocol", help_text="Rx To FC")

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver'

        verbose_name = 'Receiver'
        verbose_name_plural = 'Receivers'
        ordering = ['manufacturer', 'model', ]


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

    def delete(self, *args, **kwargs):
        if self.receiver.receiver_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only ReceiverDetail for this Receiver.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_detail'

        verbose_name = 'Receiver Detail'
        verbose_name_plural = 'Receiver Details'
        ordering = ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip']
        unique_together = ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip']


class ReceiverProtocolType(models.Model):
    type = models.CharField(max_length=50, verbose_name="Output Protocol Type", help_text="Rx To FC")
    is_public = models.BooleanField(default=False, help_text="Is public?")

    def __str__(self):
        return self.type

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_protocol_type'

        verbose_name = 'Receiver Protocol Type'
        verbose_name_plural = 'Receiver Protocol Types'
        ordering = ['type', '-is_public']
