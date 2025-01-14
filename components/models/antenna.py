from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.mixins.base_antenna_mixins import BaseAntennaMixin, BaseAntennaDetailMixin, BaseAntennaConnectorMixin, \
    BaseAntennaTypeMixin


class Antenna(BaseComponentMixin, BaseAntennaMixin):

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('api:v1:components:antenna-detail', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna'

        verbose_name = _('Antenna')
        verbose_name_plural = _('Antennas')
        ordering = ['manufacturer', 'model', ]
        unique_together = (('manufacturer', 'model'),)


class AntennaType(BaseModelMixin, BaseAntennaTypeMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_type'

        verbose_name = _('Antenna Type')
        verbose_name_plural = _('Antenna Types')
        ordering = ['type']


class AntennaDetail(BaseModelMixin, BaseAntennaDetailMixin):

    antenna = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='details')

    def delete(self, *args, **kwargs):
        if self.antenna.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only AntennaDetail for this Antenna."), self)

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_detail'

        verbose_name = _('Antenna Detail')
        verbose_name_plural = _('Antenna Details')
        ordering = ['antenna', 'connector_type']
        unique_together = ('antenna', 'connector_type', 'angle_type')


class AntennaConnector(BaseModelMixin, BaseAntennaConnectorMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_antenna_connector'

        verbose_name = _('Antenna Connector')
        verbose_name_plural = _('Antenna Connectors')
        ordering = ['type', ]
