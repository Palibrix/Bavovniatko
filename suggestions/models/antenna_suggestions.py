from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from components.mixins import BaseComponentMixin, BaseModelMixin
from components.mixins.base_antenna_mixins import BaseAntennaMixin, BaseAntennaTypeMixin, BaseAntennaConnectorMixin, \
    BaseAntennaDetailMixin
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from suggestions.mixins import BaseSuggestionMixin, BaseSuggestionFilesDeletionMixin


class AntennaSuggestion(BaseSuggestionFilesDeletionMixin, BaseComponentMixin, BaseAntennaMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Antenna', blank=True, null=True, related_name='submitted_suggestions',
                                     on_delete=models.CASCADE)

    def clean(self):
        if not self.bandwidth_min <= self.center_frequency <= self.bandwidth_max:
            raise ValidationError(_("Max frequency must be higher or equal to min frequency and "
                                  "center_frequency must be between them."))

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()
        antenna, created = Antenna.objects.update_or_create(
            id=self.related_instance_id,
            defaults={
                'manufacturer': self.manufacturer,
                'model': self.model,
                'description': self.description,
                'type': self.type,
                'center_frequency': self.center_frequency,
                'bandwidth_min': self.bandwidth_min,
                'bandwidth_max': self.bandwidth_max,
                'swr': self.swr,
                'gain': self.gain,
                'radiation': self.radiation,
            }
        )

        antenna.full_clean()
        antenna.save()
        if created:
            self.related_instance = antenna
            self.save()

        for suggested_image in self.suggested_images.all():
            if not suggested_image.object:
                suggested_image.object = antenna
            suggested_image.save()

        for suggested_document in self.suggested_documents.all():
            if not suggested_document.object:
                suggested_document.object = antenna
            suggested_document.save()

        for suggested_detail in self.suggested_details.all():
            antenna_detail, created = AntennaDetail.objects.update_or_create(
                id=suggested_detail.related_instance_id,
                antenna=antenna,
                defaults={
                    'connector_type': suggested_detail.connector_type,
                    'weight': suggested_detail.weight,
                    'angle_type': suggested_detail.angle_type,
                }
            )
            antenna_detail.full_clean()
            antenna_detail.save()

            if created:
                suggested_detail.related_instance = antenna_detail
                suggested_detail.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna'

        verbose_name = _('Antenna Suggestion')
        verbose_name_plural = _('Antenna Suggestions')
        ordering = ['manufacturer', 'model', ]
        unique_together = (('manufacturer', 'model'),)


class AntennaTypeSuggestion(BaseModelMixin, BaseAntennaTypeMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.AntennaType', blank=True, null=True, related_name='submitted_suggestions',
                                     on_delete=models.CASCADE)

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()

        antenna_type, created = AntennaType.objects.update_or_create(
            id = self.related_instance_id,
            defaults={
                'type': self.type,
                'direction': self.direction,
                'polarization': self.polarization,
            }
        )
        antenna_type.save()
        if created:
            self.related_instance = antenna_type
            self.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna_type'

        verbose_name = _('Antenna Type Suggestion')
        verbose_name_plural = _('Antenna Type Suggestions')
        ordering = ['type']


class AntennaConnectorSuggestion(BaseModelMixin, BaseAntennaConnectorMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.AntennaConnector', blank=True, null=True, related_name='submitted_suggestions',
                                     on_delete=models.CASCADE)

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()

        antenna_connector, created = AntennaConnector.objects.update_or_create(
            id = self.related_instance_id,
            defaults={
                'type': self.type
            }
        )
        antenna_connector.save()
        if created:
            self.related_instance = antenna_connector
            self.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_antenna_connector'

        verbose_name = _('Antenna Connector Suggestion')
        verbose_name_plural = _('Antenna Connector Suggestions')
        ordering = ['type']


class ExistingAntennaDetailSuggestion(BaseModelMixin, BaseAntennaDetailMixin, BaseSuggestionMixin):
    """ Suggest new detail to existing antenna """
    antenna = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='suggested_details',
                                verbose_name='Antenna')
    related_instance = models.ForeignKey('components.AntennaDetail', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='suggested_details')

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()

        antenna_detail, created = AntennaDetail.objects.update_or_create(
            antenna = self.antenna,
            id = self.related_instance_id,
            defaults={
                'connector_type': self.connector_type,
                'weight': self.weight,
                'angle_type': self.angle_type,
            }
        )
        antenna_detail.save()

        if created:
            self.related_instance = antenna_detail
            self.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_antenna_detail'

        verbose_name = _('Existing Antenna Detail Suggestion')
        verbose_name_plural = _('Existing Antenna Detail Suggestions')
        ordering = ['antenna', 'connector_type']
        unique_together = ('antenna', 'connector_type', 'angle_type')


class SuggestedAntennaDetailSuggestion(BaseModelMixin, BaseAntennaDetailMixin):
    """ Add detail to suggested antenna """
    suggestion = models.ForeignKey('suggestions.AntennaSuggestion', on_delete=models.CASCADE, related_name='suggested_details', verbose_name='details')
    related_instance = models.ForeignKey('components.AntennaDetail', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='submitted_suggestions', verbose_name='submitted_suggestions')

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_antenna_detail'

        verbose_name = _('Suggested Antenna Detail')
        verbose_name_plural = _('Suggested Antenna Details')
        ordering = ['related_instance', 'connector_type']
        unique_together = ('related_instance', 'connector_type', 'angle_type')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only AntennaDetail for this Antenna."), self)
