from django.contrib import admin
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin


class Battery(BaseComponentMixin):

    class Types(models.TextChoices):
        LIPO = 'LIPO', _('LiPo')
        LI_ION = 'LI_ION', _('Li-Ion')
        LIHV = 'LIHV', _('LiHV')
        Another = 'ANOTHER', _('Another')

    # drone = models.OneToOneField('Drone', on_delete=models.CASCADE, related_name='battery')

    model = None
    series = models.PositiveSmallIntegerField(verbose_name='Cells in series',
                                              help_text=_('Number of cells in series, e.g. 6 from 6S3P'))
    parallels = models.PositiveSmallIntegerField(verbose_name='Cells in parallels',
                                                 help_text=_('Number of cells in parallels, e.g. 3 form 6S3P'))

    size = models.CharField(max_length=5, validators=[MinLengthValidator(5)],
                            help_text=_('Size of individual battery (e.g. 18650)'))
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.LIPO)
    connector_type = models.CharField(max_length=50, verbose_name=_('Power Connector'),
                                      help_text=_('Power Connector Type (e.g. XT60)'),
                                      blank=True, null=True)
    balancer = models.CharField(max_length=50, verbose_name=_('Charge Balancer'),
                                help_text=_('Charge Balancer, e.g. JST XH-7 pin'),
                                blank=True, null=True)

    capacity = models.IntegerField(verbose_name=_('Battery Capacity, mAh'),
                                   help_text=_('Battery Capacity, mAh'))
    voltage = models.FloatField(validators=[MinValueValidator(2), MaxValueValidator(28)],
                                help_text=_('Rated Voltage'), verbose_name=_('Rated Voltage, V'))

    discharge_current = models.IntegerField(help_text=_('Max. discharge current, A'),
                                            verbose_name=_('Max. discharge current'))
    charge_current = models.IntegerField(help_text=_('Max. charge current, A'),
                                         verbose_name=_('Max. charge current'))

    weight = models.FloatField(help_text=_('Weight oh the camera in grams'))

    length = models.FloatField(help_text=_('Length of the battery, mm'))
    height = models.FloatField(help_text=_('Height of the battery, mm'))
    width = models.FloatField(help_text=_('Width of the battery, mm'))

    def __str__(self):
        return (f'{self.get_configuration} {self.capacity}mAh {self.size} '
                f'{self.type}')

    @property
    @admin.display(description='Physical Dimensions')
    def get_dimensions(self):
        return _(f'L{self.length} x H{self.height} x W{self.width}')

    @property
    @admin.display(description='Configuration')
    def get_configuration(self):
        return f'{self.series}S{self.parallels}P'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_battery'

        verbose_name = _('Battery')
        verbose_name_plural = _('Batteries')
        ordering = ('size', 'capacity')
