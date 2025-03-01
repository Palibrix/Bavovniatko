from django.contrib import admin

from components.mixins.admin.base_transmitter_admin_mixins import TransmitterAdminMixin, OutputPowerAdminMixin
from components.models.transmitter import OutputPower, Transmitter
from documents.admin.components_admin import TransmitterDocumentInline
from galleries.admin.components_admin import TransmitterGalleryInline


@admin.register(Transmitter)
class TransmitterAdmin(TransmitterAdminMixin):
    inlines = [TransmitterGalleryInline, TransmitterDocumentInline]


@admin.register(OutputPower)
class OutputPowerAdmin(OutputPowerAdminMixin):
    pass