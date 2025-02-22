from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin


class BaseAntennaMixin(BaseComponentMixin):
    ANTENNA_FIELDS = [
        'manufacturer', 'model', 'description',
        'type', 'center_frequency', 'bandwidth_min', 'bandwidth_max',
        'swr', 'gain', 'radiation'
    ]

    class AxialRatioChoice(models.TextChoices):
        NOT_SPECIFIED = 'not_specified', _('Not Specified (For LP antennas ONLY)')
        IDEAL = 'ideal', _('Ideal (1)')
        CLOSE = 'close', _('Close to 1')

    type = models.ForeignKey('components.AntennaType', on_delete=models.PROTECT)

    center_frequency = models.FloatField(help_text=_("Center frequency of the antenna"),
                                         )
    bandwidth_min = models.FloatField(help_text=_("Min. bandwidth (frequency) of the antenna"), )
    bandwidth_max = models.FloatField(help_text=_("Max. bandwidth (frequency) of the antenna"), )

    swr = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                            help_text=_("SWR of the antenna at Center Frequency (lower=better)"),
                            verbose_name=_('SWR (VSWR)'),
                            blank=True, null=True)

    gain = models.FloatField(validators=[MinValueValidator(0)], help_text=_("Gain of the antenna, in dBi"),
                             blank=True, null=True)

    radiation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                    help_text=_("Radiation efficiency of the antenna, in %"),
                                    blank=True, null=True)

    @property
    @admin.display(description=_('Bandwidth Range'))
    def get_bandwidth(self):
        return f'{self.bandwidth_min} - {self.bandwidth_max}'

    def clean(self):
        if not self.bandwidth_min <= self.center_frequency <= self.bandwidth_max:
            raise ValidationError(_("Max frequency must be higher or equal to min frequency and "
                                  "center_frequency must be between them."))

    class Meta:
        abstract = True


class BaseAntennaDetailMixin(BaseModelMixin):
    DETAIL_FIELDS = ['connector_type', 'weight', 'angle_type']

    class ConnectorChoice(models.TextChoices):
        ANGLED = 'angled', _('Angled')
        STRAIGHT = 'straight', _('Straight')

    connector_type = models.ForeignKey('components.AntennaConnector', on_delete=models.PROTECT)
    weight = models.FloatField(help_text=_('Weight of the antenna in grams'), )
    angle_type = models.CharField(max_length=50, choices=ConnectorChoice.choices,
                                  default=ConnectorChoice.STRAIGHT,
                                  help_text=_("Angled or Straight"))

    def __str__(self):
        return f"{self.connector_type}, {self.angle_type}"

    class Meta:
        abstract = True


class BaseAntennaTypeMixin(BaseModelMixin):
    TYPE_FIELDS = ['type', 'direction', 'polarization']

    class DirectionalityChoice(models.TextChoices):
        DIRECTIONAL = 'directional', _('Directional')
        OMNI_DIRECTIONAL = 'omni', _('Omni-directional')

    class PolarizationChoice(models.TextChoices):
        LINEAR = 'linear', _('Linear, LP')
        LEFT_CIRCULAR = 'left_circular', 'Left-hand Circular, LHCP'
        RIGHT_CIRCULAR = 'right_circular', 'Right-hand Circular, RHCP'

    type = models.CharField(max_length=50, unique=True,
                            help_text=_("Type of the antenna, e.g. Monopole, Dipole etc."))
    direction = models.CharField(max_length=50, choices=DirectionalityChoice.choices,
                                 default=DirectionalityChoice.DIRECTIONAL,
                                 help_text=_("Omni-directional: all directions, Directional: one direction."))
    polarization = models.CharField(max_length=50, choices=PolarizationChoice.choices,
                                    default=PolarizationChoice.LINEAR)

    def __str__(self):
        return f"{self.type}, {self.direction} {self.polarization}"

    class Meta:
        abstract = True


class BaseAntennaConnectorMixin(BaseModelMixin):
    CONNECTOR_FIELDS = ['type']

    type = models.CharField(max_length=50, help_text=_("Type of antenna connector"), unique=True)

    def __str__(self):
        return self.type

    class Meta:
        abstract = True
