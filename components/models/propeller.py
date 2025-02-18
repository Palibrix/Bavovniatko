from django.utils.translation import gettext_lazy as _

from components.mixins.base_propeller_mixins import BasePropellerMixin


class Propeller(BasePropellerMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_propeller'

        verbose_name = _('Propeller')
        verbose_name_plural = _('Propellers')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)
