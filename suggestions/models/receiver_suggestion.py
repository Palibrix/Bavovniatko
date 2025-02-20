from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_receiver_mixins import (
    BaseReceiverMixin,
    BaseReceiverDetailMixin,
    BaseProtocolTypeMixin
)
from components.models import (
    Receiver,
    ReceiverDetail,
    ReceiverProtocolType
)
from suggestions.mixins import (
    BaseSuggestionMixin,
    SuggestionFilesDeletionMixin,
    MediaHandlerMixin
)


class ReceiverSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseReceiverMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey(
        'components.Receiver',
        blank=True,
        null=True,
        related_name='submitted_suggestions',
        on_delete=models.CASCADE
    )

    def _handle_post_accept(self, instance):
        self._handle_media(instance)
        self._handle_details(instance)

    def _handle_details(self, instance):
        for suggested_detail in self.suggested_details.all():
            receiver_detail = ReceiverDetail.objects.create(
                receiver=instance,
                **{field: getattr(suggested_detail, field)
                   for field in BaseReceiverDetailMixin.DETAIL_FIELDS}
            )
            receiver_detail.full_clean()
            receiver_detail.save()

            suggested_detail.related_instance = receiver_detail
            suggested_detail.save()

    def _create_instance(self):
        instance = Receiver.objects.create(
            **{field: getattr(self, field)
               for field in self.RECEIVER_FIELDS
               if field not in ['antenna_connectors', 'protocols']}
        )

        instance.full_clean()
        instance.save()

        if hasattr(self, 'antenna_connectors') and self.antenna_connectors.exists():
            instance.antenna_connectors.set(self.antenna_connectors.all())

        if hasattr(self, 'protocols') and self.protocols.exists():
            instance.protocols.set(self.protocols.all())

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_receiver'
        verbose_name = _('Receiver Suggestion')
        verbose_name_plural = _('Receiver Suggestions')
        ordering = ['manufacturer', 'model']


class ReceiverProtocolTypeSuggestion(BaseProtocolTypeMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey(
        'components.ReceiverProtocolType',
        blank=True,
        null=True,
        related_name='submitted_suggestions',
        on_delete=models.CASCADE
    )

    def _create_instance(self):
        instance = ReceiverProtocolType.objects.create(
            **{field: getattr(self, field)
               for field in self.PROTOCOL_FIELDS}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_receiver_protocol_type'
        verbose_name = _('Receiver Protocol Type Suggestion')
        verbose_name_plural = _('Receiver Protocol Type Suggestions')
        ordering = ['type']


class ExistingReceiverDetailSuggestion(BaseReceiverDetailMixin, BaseSuggestionMixin):
    """Suggest new detail to existing receiver"""
    receiver = models.ForeignKey(
        'components.Receiver',
        on_delete=models.CASCADE,
        related_name='suggested_details',
        verbose_name='Receiver'
    )
    related_instance = models.ForeignKey(
        'components.ReceiverDetail',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='suggested_details'
    )

    def _create_instance(self):
        instance = ReceiverDetail.objects.create(
            receiver=self.receiver,
            **{field: getattr(self, field)
               for field in self.DETAIL_FIELDS}
        )
        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_receiver_detail'
        verbose_name = _('Existing Receiver Detail Suggestion')
        verbose_name_plural = _('Existing Receiver Detail Suggestions')
        ordering = ['receiver', 'frequency']


class SuggestedReceiverDetailSuggestion(BaseReceiverDetailMixin):
    """Add detail to suggested receiver"""
    suggestion = models.ForeignKey(
        'suggestions.ReceiverSuggestion',
        on_delete=models.CASCADE,
        related_name='suggested_details',
        verbose_name='details'
    )
    related_instance = models.ForeignKey(
        'components.ReceiverDetail',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='submitted_suggestions',
        verbose_name='submitted_suggestions'
    )

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(
                _("Cannot delete the only Detail for this object."),
                self
            )

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_receiver_detail'
        verbose_name = _('Suggested Receiver Detail')
        verbose_name_plural = _('Suggested Receiver Details')
        ordering = ['related_instance', 'frequency']