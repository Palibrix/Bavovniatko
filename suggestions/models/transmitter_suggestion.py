from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins.base_transmitter_mixins import BaseTransmitterMixin, BaseOutputPowerMixin
from components.models import Transmitter, OutputPower
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin, MediaHandlerMixin


class TransmitterSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseTransmitterMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Transmitter', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)

    def _create_instance(self):
        instance = Transmitter.objects.create(
            **{field: getattr(self, field)
               for field in self.TRANSMITTER_FIELDS}
        )

        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()

        if hasattr(self, 'video_formats') and self.video_formats.exists():
            instance.video_formats.set(self.video_formats.all())
        if hasattr(self, 'output_powers') and self.output_powers.exists():
            instance.output_powers.set(self.output_powers.all())
        if hasattr(self, 'antenna_connectors') and self.antenna_connectors.exists():
            instance.antenna_connectors.set(self.antenna_connectors.all())

        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_transmitter'
        verbose_name = _('Transmitter Suggestion')
        verbose_name_plural = _('Transmitter Suggestions')
        ordering = ['manufacturer', 'model']


class OutputPowerSuggestion(BaseOutputPowerMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.OutputPower', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = OutputPower.objects.create(
            **{field: getattr(self, field)
               for field in self.OUTPUT_POWER_FIELDS}
        )

        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_output_power'
        verbose_name = _('Output Power Suggestion')
        verbose_name_plural = _('Output Power Suggestions')
        ordering = ['output_power']