from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from components.mixins import BaseComponentMixin, BaseModelMixin
from components.mixins.base_antenna_mixins import BaseAntennaMixin, BaseAntennaTypeMixin, BaseAntennaConnectorMixin, \
    BaseAntennaDetailMixin
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from suggestions.mixins import BaseSuggestionMixin


class AntennaSuggestion(BaseComponentMixin, BaseAntennaMixin, BaseSuggestionMixin):

    def clean(self):
        if not self.bandwidth_min <= self.center_frequency <= self.bandwidth_max:
            raise ValidationError(_("Max frequency must be higher or equal to min frequency and "
                                  "center_frequency must be between them."))

    def accept(self):
        with transaction.atomic():
            self.reviewed = True
            self.save()

            antenna = Antenna(
                manufacturer=self.manufacturer,
                model=self.model,
                description=self.description,
                type = self.type,
                center_frequency = self.center_frequency,
                bandwidth_min = self.bandwidth_min,
                bandwidth_max = self.bandwidth_max,
                swr=self.swr,
                gain=self.gain,
                radiation=self.radiation,
            )
            antenna.full_clean()
            antenna.save()

            for suggested_detail in self.suggested_details.all():
                antenna_detail = AntennaDetail(
                    antenna=antenna,
                    connector_type=suggested_detail.connector_type,
                    weight=suggested_detail.weight,
                    angle_type=suggested_detail.angle_type,
                )
                antenna_detail.full_clean()
                antenna_detail.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna'

        verbose_name = _('Antenna Suggestion')
        verbose_name_plural = _('Antenna Suggestions')
        ordering = ['manufacturer', 'model', ]
        unique_together = (('manufacturer', 'model'),)


class AntennaTypeSuggestion(BaseModelMixin, BaseAntennaTypeMixin, BaseSuggestionMixin):

    def accept(self):
        self.reviewed = True
        self.save()

        antenna_type = AntennaType(
            type = self.type,
            direction = self.direction,
            polarization = self.polarization,
        )
        antenna_type.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna_type'

        verbose_name = _('Antenna Type Suggestion')
        verbose_name_plural = _('Antenna Type Suggestions')
        ordering = ['type']

class AntennaConnectorSuggestion(BaseModelMixin, BaseAntennaConnectorMixin, BaseSuggestionMixin):

    def accept(self):
        self.reviewed = True
        self.save()

        antenna_connector = AntennaConnector(
            type = self.type
        )
        antenna_connector.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna_connector'

        verbose_name = _('Antenna Connector Suggestion')
        verbose_name_plural = _('Antenna Connector Suggestions')
        ordering = ['type']


class ExistingAntennaDetailSuggestion(BaseModelMixin, BaseAntennaDetailMixin, BaseSuggestionMixin):
    """ Suggest new detail to existing antenna """
    antenna = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='suggested_details')

    def accept(self):
        self.reviewed = True
        self.save()

        antenna_detail = AntennaDetail(
            antenna = self.antenna,
            connector_type = self.connector_type,
            weight = self.weight,
            angle_type = self.angle_type,
        )
        antenna_detail.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_antenna_detail'

        verbose_name = _('Existing Antenna Detail Suggestion')
        verbose_name_plural = _('Existing Antenna Detail Suggestions')
        ordering = ['antenna', 'connector_type']
        unique_together = ('antenna', 'connector_type', 'angle_type')


class SuggestedAntennaDetailSuggestion(BaseModelMixin, BaseAntennaDetailMixin):
    """ Add detail to suggested antenna """
    antenna = models.ForeignKey('suggestions.AntennaSuggestion', on_delete=models.CASCADE, related_name='suggested_details', verbose_name='details')

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_antenna_detail'

        verbose_name = _('Suggested Antenna Detail')
        verbose_name_plural = _('Suggested Antenna Details')
        ordering = ['antenna', 'connector_type']
        unique_together = ('antenna', 'connector_type', 'angle_type')