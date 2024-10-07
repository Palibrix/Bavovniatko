from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin


class Propeller(BaseComponentMixin):

    size = models.IntegerField(validators=[MinValueValidator(2)],
                               help_text=_("Size of the propeller in inches"))
    pitch = models.FloatField(help_text=_("Pitch of the propeller in inches"))
    blade_count = models.CharField(max_length=8,
                                   choices=[(str(i), str(i)) for i in range(2, 9)] + [('another', _('Another'))], )
    weight = models.FloatField(help_text=_("Weight of propeller in grams"),
                               blank=True, null=True)

    class Meta:
        app_label = 'components'
        db_table = 'components_propeller'

        verbose_name = _('Propeller')
        verbose_name_plural = _('Propellers')
