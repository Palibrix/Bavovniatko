from django.db import models
from django.utils.translation import gettext_lazy as _

from components.mixins.base_receiver_mixins import (
    BaseReceiverMixin,
    BaseReceiverDetailMixin,
    BaseProtocolTypeMixin
)


class Receiver(BaseReceiverMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_receiver'
        verbose_name = _('Receiver')
        verbose_name_plural = _('Receivers')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class ReceiverDetail(BaseReceiverDetailMixin):
    receiver = models.ForeignKey('components.Receiver',
                                on_delete=models.CASCADE,
                                related_name='details')

    def delete(self, *args, **kwargs):
        if self.receiver.details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(
                _("Cannot delete the only ReceiverDetail for this Receiver."),
                self
            )

    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_detail'
        verbose_name = _('Receiver Detail')
        verbose_name_plural = _('Receiver Details')
        ordering = ['receiver', 'frequency']
        unique_together = ('receiver', 'frequency')


class ReceiverProtocolType(BaseProtocolTypeMixin):
    class Meta:
        app_label = 'components'
        db_table = 'components_receiver_protocol_type'
        verbose_name = _('Receiver Protocol Type')
        verbose_name_plural = _('Receiver Protocol Types')
        ordering = ['type']