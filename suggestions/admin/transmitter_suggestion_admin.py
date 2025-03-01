from django.contrib import admin

from components.mixins.admin.base_transmitter_admin_mixins import (
    TransmitterAdminMixin, OutputPowerAdminMixin
)
from documents.admin.components_admin import TransmitterDocumentInline
from galleries.admin.components_admin import TransmitterGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    TransmitterSuggestion, OutputPowerSuggestion
)


@admin.register(TransmitterSuggestion)
class TransmitterSuggestionAdmin(BaseSuggestionAdminMixin, TransmitterAdminMixin):
    inlines = [TransmitterGalleryInline, TransmitterDocumentInline]
    list_display = TransmitterAdminMixin.list_display + ('status', 'user')
    list_filter = TransmitterAdminMixin.list_filter + ('status', 'user')
    readonly_fields = TransmitterAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(OutputPowerSuggestion)
class OutputPowerSuggestionAdmin(BaseSuggestionAdminMixin, OutputPowerAdminMixin):
    list_display = OutputPowerAdminMixin.list_display + ('status', 'user')
    list_filter = ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
