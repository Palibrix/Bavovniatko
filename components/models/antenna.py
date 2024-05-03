from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from components.mixins import UniqueItemConstraintMixin, UniqueConstraintMixin

User = get_user_model()


class Antenna(models.Model, UniqueConstraintMixin):
    fields_public = ['manufacturer', 'model',
                     'type',
                     'center_frequency', 'bandwidth_min', 'bandwidth_max',
                     'swr', 'gain', 'radiation'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = 'An Antenna with these attributes already exists for this user.'

    class AxialRatioChoice(models.TextChoices):
        NOT_SPECIFIED = 'not_specified', 'Not Specified (For LP antennas ONLY)'
        IDEAL = 'ideal', 'Ideal (1)'
        CLOSE = 'close', 'Close to 1'

    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text="Full name of the item")

    type = models.ForeignKey('AntennaType', on_delete=models.PROTECT)

    center_frequency = models.FloatField(help_text="Center frequency of the antenna",
                                         )
    bandwidth_min = models.FloatField(help_text="Minimum bandwidth (frequency) of the antenna",)
    bandwidth_max = models.FloatField(help_text="Maximum bandwidth (frequency) of the antenna",)

    swr = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                            help_text="SWR of the antenna at Center Frequency (lower=better)",
                            verbose_name='SWR (VSWR)',
                            blank=True, null=True)

    gain = models.FloatField(validators=[MinValueValidator(0)], help_text="Gain of the antenna, in dBi",)

    radiation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                    help_text="Radiation efficiency of the antenna, in %",)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Public if empty",
                             blank=True, null=True)

    def __str__(self):
        return self.model

    def clean(self):
        if not self.bandwidth_min <= self.center_frequency <= self.bandwidth_max:
            raise ValidationError("Max frequency must be higher or equal to min frequency and "
                                  "center_frequency must be between them.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna'

        verbose_name = 'Antenna'
        verbose_name_plural = 'Antennas'
        ordering = ['manufacturer', 'model', ]


class AntennaType(models.Model, UniqueItemConstraintMixin):
    fields = ['type', 'direction', 'polarization']

    error_message = 'A Antenna Type with these attributes already exists for public use.'

    class DirectionalityChoice(models.TextChoices):
        DIRECTIONAL = 'directional', 'Directional'
        OMNI_DIRECTIONAL = 'omni', 'Omni-directional'

    class PolarizationChoice(models.TextChoices):
        LINEAR = 'linear', 'Linear, LP'
        CIRCULAR = 'circular', 'Circular'

    type = models.CharField(max_length=50, help_text="Type of antenna")
    direction = models.CharField(max_length=50, choices=DirectionalityChoice.choices,
                                 default=DirectionalityChoice.DIRECTIONAL,
                                 help_text="Omni-directional: all directions, Directional: one direction.")
    polarization = models.CharField(max_length=50, choices=PolarizationChoice.choices,
                                    default=PolarizationChoice.LINEAR)

    is_public = models.BooleanField(default=False, help_text="Is public?")

    def __str__(self):
        return f"{self.type}, {self.direction} {self.polarization}"

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_type'

        verbose_name = 'Antenna Type'
        verbose_name_plural = 'Antenna Types'
        ordering = ['type']


class AntennaDetail(models.Model):

    class ConnectorChoice(models.TextChoices):
        ANGLED = 'angled', 'Angled'
        STRAIGHT = 'straight', 'Straight'

    antenna = models.ForeignKey(Antenna, on_delete=models.CASCADE, related_name='antenna_details')

    connector_type = models.ForeignKey('AntennaConnector', on_delete=models.PROTECT)
    weight = models.FloatField(help_text='Weight of the antenna in grams', )
    angle_type = models.CharField(max_length=50, choices=ConnectorChoice.choices,
                                  default=ConnectorChoice.STRAIGHT,
                                  help_text="Angled or Straight")

    def __str__(self):
        return f"{self.connector_type}, {self.angle_type}"

    def delete(self, *args, **kwargs):
        if self.antenna.antenna_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError("Cannot delete the only FrameDetail for this Frame.", self)

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_detail'

        verbose_name = 'Antenna Detail'
        verbose_name_plural = 'Antenna Details'
        ordering = ['antenna', 'connector_type']
        unique_together = ('antenna', 'connector_type', 'angle_type')


class AntennaConnector(models.Model):
    type = models.CharField(max_length=50, help_text="Type of antenna connector")
    is_public = models.BooleanField(default=False, help_text="Is public?")

    def __str__(self):
        return self.type

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_connector'

        verbose_name = 'Antenna Connector'
        verbose_name_plural = 'Antenna Connectors'
        ordering = ['type', '-is_public']
