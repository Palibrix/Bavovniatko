from django.contrib import admin
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.models import Battery


class BaseMotorMixin(BaseComponentMixin):
    MOTOR_FIELDS = [
        'manufacturer', 'model', 'description',
        'stator_diameter', 'stator_height', 'configuration',
        'mount_height', 'mount_width'
    ]

    stator_diameter = models.CharField(max_length=2, validators=[MinLengthValidator(2)],
                                     help_text=_("Two first digits of size (e.g. 28 from 2806)"))
    stator_height = models.CharField(max_length=4, validators=[MinLengthValidator(2)],
                                   help_text=_("Two last digits of size (e.g. 06 from 2806 or 06.5 from 2806.5)"))

    configuration = models.CharField(max_length=50, help_text=_('Configuration of the motor (e.g. 12N14P)'))

    mount_height = models.FloatField(max_length=5, help_text=_("Height of the motor in mm"),
                                   verbose_name=_("Motor mount size height"))
    mount_width = models.FloatField(max_length=5, help_text=_("Width of the motor in mm"),
                                  verbose_name=_("Motor mount size width"))

    @property
    @admin.display(description=_("Motor Mount Size"))
    def get_mount_dimensions(self):
        return f'{self.mount_width}x{self.mount_height} mm'

    @property
    @admin.display(description=_('Stator Size'))
    def get_stator_size(self):
        return f'{self.stator_diameter}{self.stator_height}'

    def __str__(self):
        return f'{self.manufacturer} {self.model} {self.get_stator_size}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseMotorDetailMixin(BaseModelMixin):
    DETAIL_FIELDS = [
        'weight', 'max_power', 'kv_per_volt', 'peak_current',
        'idle_current', 'resistance', 'voltage'
    ]

    weight = models.FloatField(validators=[MinValueValidator(0)], help_text=_("Motor weight in grams"))
    max_power = models.PositiveIntegerField(help_text=_("Max power, W"))
    kv_per_volt = models.PositiveIntegerField(help_text=_("KV per volt"),
                                            verbose_name='KV per volt')

    peak_current = models.FloatField(validators=[MinValueValidator(0)], help_text=_("Peak current of the motor, A"),
                                   blank=True, null=True)
    idle_current = models.FloatField(validators=[MinValueValidator(0)], help_text=_("Idle current of the motor, A"),
                                   blank=True, null=True)

    resistance = models.FloatField(validators=[MinValueValidator(0)], help_text=_("Resistance, in mΩ (mOhm)"),
                                 verbose_name=_('Internal Resistance'), blank=True, null=True)

    voltage = models.ForeignKey('components.RatedVoltage', on_delete=models.PROTECT, related_name='%(class)s_rated_voltage')

    def __str__(self):
        return f'{self.get_kv_per_volt} {self.voltage.max_cells}S'

    @property
    def get_kv_per_volt(self):
        return f'KV{self.kv_per_volt}'

    @property
    def get_weight(self):
        return f'{self.weight}g'

    @property
    def get_max_power(self):
        return f'{self.max_power}W'

    @property
    def get_peak_current(self):
        return f'{self.peak_current}A'

    @property
    def get_idle_current(self):
        return f'{self.idle_current}A'

    @property
    def get_resistance(self):
        return f'{self.resistance}mOhm'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseRatedVoltageMixin(BaseModelMixin):
    VOLTAGE_FIELDS = ['min_cells', 'max_cells', 'type']

    min_cells = models.IntegerField(validators=[MinValueValidator(1)], default=1,
                                  verbose_name=_('Min. number of cells'),
                                  help_text=_('Number of min. possible quantity of cells in series'))
    max_cells = models.IntegerField(validators=[MinValueValidator(1)], default=1,
                                  verbose_name=_('Max. number of cells'),
                                  help_text=_('Number of max. possible quantity of cells in series'))
    type = models.CharField(max_length=10, choices=Battery.Types.choices, default=Battery.Types.LIPO)

    def __str__(self):
        return f'{self.get_cells} {self.type}'

    @property
    def get_min_cells(self):
        return f'{self.min_cells}S'

    @property
    def get_max_cells(self):
        return f'{self.max_cells}S'

    @property
    @admin.display(description=_('Number of cells in series'))
    def get_cells(self):
        return f'{self.get_min_cells}-{self.get_max_cells}'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True