from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_antenna_mixins import BaseAntennaMixin, BaseAntennaTypeMixin, BaseAntennaConnectorMixin, \
    BaseAntennaDetailMixin
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin


class AntennaSuggestion(SuggestionFilesDeletionMixin, BaseAntennaMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Antenna', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)
        self._handle_details(instance)

    def _handle_media(self, antenna):
        for suggested_image in self.suggested_images.all():
            if not suggested_image.object:
                suggested_image.object = antenna
            suggested_image.save()

        for suggested_document in self.suggested_documents.all():
            if not suggested_document.object:
                suggested_document.object = antenna
            suggested_document.save()

    def _handle_details(self, antenna):
        for suggested_detail in self.suggested_details.all():
            antenna_detail = AntennaDetail.objects.create(
                antenna=antenna,
                **{field: getattr(suggested_detail, field)
                   for field in BaseAntennaDetailMixin.DETAIL_FIELDS}
            )
            antenna_detail.full_clean()
            antenna_detail.save()

            suggested_detail.related_instance = antenna_detail
            suggested_detail.save()

    def _create_instance(self):
        antenna = Antenna.objects.create(
            **{field: getattr(self, field)
               for field in self.ANTENNA_FIELDS}
        )

        antenna.full_clean()
        antenna.save()

        self.related_instance = antenna
        self.save()
        return antenna


class AntennaTypeSuggestion(BaseAntennaTypeMixin, BaseSuggestionMixin):

    related_instance = models.ForeignKey('components.AntennaType', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        antenna_type = AntennaType.objects.create(
            **{field: getattr(self, field)
               for field in self.TYPE_FIELDS}
        )

        antenna_type.full_clean()
        antenna_type.save()

        self.related_instance = antenna_type
        self.save()
        return antenna_type


class AntennaConnectorSuggestion(BaseAntennaConnectorMixin, BaseSuggestionMixin):

    related_instance = models.ForeignKey('components.AntennaConnector', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        antenna_connector = AntennaConnector.objects.create(
            **{field: getattr(self, field)
               for field in self.CONNECTOR_FIELDS}
        )

        antenna_connector.full_clean()
        antenna_connector.save()

        self.related_instance = antenna_connector
        self.save()
        return antenna_connector


class ExistingAntennaDetailSuggestion(BaseAntennaDetailMixin, BaseSuggestionMixin):
    """ Suggest new detail to existing antenna """

    antenna = models.ForeignKey('components.Antenna', on_delete=models.CASCADE,
                                related_name='suggested_details',
                                verbose_name='Antenna')
    related_instance = models.ForeignKey('components.AntennaDetail', on_delete=models.CASCADE,
                                         blank=True, null=True,
                                         related_name='suggested_details')

    def _create_instance(self):
        antenna_detail = AntennaDetail.objects.create(
            antenna=self.antenna,
            **{field: getattr(self, field)
               for field in self.DETAIL_FIELDS}
        )

        antenna_detail.full_clean()
        antenna_detail.save()

        self.related_instance = antenna_detail
        self.save()
        return antenna_detail

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_antenna_detail'

        verbose_name = _('Existing Antenna Detail Suggestion')
        verbose_name_plural = _('Existing Antenna Detail Suggestions')
        ordering = ['antenna', 'connector_type']


class SuggestedAntennaDetailSuggestion(BaseAntennaDetailMixin):
    """ Add detail to suggested antenna """
    suggestion = models.ForeignKey('suggestions.AntennaSuggestion', on_delete=models.CASCADE,
                                   related_name='suggested_details',
                                   verbose_name='details')
    related_instance = models.ForeignKey('components.AntennaDetail', on_delete=models.CASCADE,
                                         blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Detail for this object."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_antenna_detail'
        verbose_name = _('Suggested Antenna Detail')
        verbose_name_plural = _('Suggested Antenna Details')
        ordering = ['related_instance', 'connector_type']
