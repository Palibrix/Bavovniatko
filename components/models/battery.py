from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import UniqueConstraintMixin

User = get_user_model()


class Battery(models.Model, UniqueConstraintMixin):
    fields_public = ['configuration', 'size', 'type', 'balancer', 'connector_type',
                     'capacity', 'voltage', 'discharge_current', 'charge_current',
                     'weight', 'length', 'height', 'thickness'
                     ]
    fields_private = fields_public + ['user', ]
    error_message = f'A {__build_class__.__name__} with these attributes already exists for this user.'

    class Types(models.TextChoices):
        LIPO = 'LIPO', 'LiPo'
        LI_ION = 'LI_ION', 'Li-Ion'
        LIHV = 'LIHV', 'LiHV'
        Another = 'ANOTHER', 'Another'

    configuration = models.CharField(verbose_name='Configuration Type', max_length=6,
                                     help_text=_('Series/Parallels e.g. 6S3P'))
    size = models.CharField(max_length=5, validators=[MinLengthValidator(5)],
                            help_text=_('Size of individual battery (e.g. 18650)'))
    type = models.CharField(max_length=10, choices=Types.choices, default=Types.LIPO)
    connector_type = models.CharField(max_length=50, verbose_name=_('Power Connector'),
                                      help_text=_('Power Connector Type (e.g. XT60)'))
    balancer = models.CharField(max_length=50, verbose_name=_('Charge Balancer'),
                                help_text=_('Charge Balancer, e.g. JST XH-7 pin'))
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
    thickness = models.FloatField(help_text=_('Thickness of the battery, mm'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_("Public if empty"),
                             blank=True, null=True)

    def __str__(self):
        return (f'{self.configuration} {self.capacity}mAh {self.size} '
                f'{self.type} {self.discharge_current}A')

    def get_params(self):
        return _(f'L{self.length} x H{self.height} x T{self.thickness}')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'components'
        db_table = 'components_battery'

        verbose_name = _('Battery')
        verbose_name_plural = _('Batteries')
        ordering = ('size', 'configuration', 'capacity')
