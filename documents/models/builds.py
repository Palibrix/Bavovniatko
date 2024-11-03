from django.db import models
from django.utils.translation import gettext_lazy as _

from documents.mixins import BaseDocumentMixin


class DroneDocument(BaseDocumentMixin):
    object = models.ForeignKey('builds.Drone', on_delete=models.CASCADE, related_name='documents')

    class Meta:
        verbose_name = _('Drone Document')
        verbose_name_plural = _('Drone Documents')
