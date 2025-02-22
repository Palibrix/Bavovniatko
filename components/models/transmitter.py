from django.utils.translation import gettext_lazy as _

from components.mixins.base_transmitter_mixins import BaseTransmitterMixin, BaseOutputPowerMixin


class Transmitter(BaseTransmitterMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_transmitter'
        verbose_name = _('Transmitter')
        verbose_name_plural = _('Transmitters')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class OutputPower(BaseOutputPowerMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_output_power'
        verbose_name = _('Output Power')
        verbose_name_plural = _('Output Powers')
        ordering = ['output_power']
