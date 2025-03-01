from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_antenna_admin_mixins import (
    AntennaAdminMixin, AntennaTypeAdminMixin, AntennaConnectorAdminMixin
)
from documents.admin.components_admin import AntennaDocumentInline
from galleries.admin.components_admin import AntennaGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    AntennaSuggestion, AntennaTypeSuggestion, AntennaConnectorSuggestion,
    ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion
)


class SuggestedAntennaDetailSuggestionInline(admin.StackedInline):
    model = SuggestedAntennaDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


@admin.register(AntennaSuggestion)
class AntennaSuggestionAdmin(BaseSuggestionAdminMixin, AntennaAdminMixin):
    inlines = [SuggestedAntennaDetailSuggestionInline, AntennaGalleryInline, AntennaDocumentInline]
    list_display = AntennaAdminMixin.list_display + ('status', 'user')
    sortable_by = AntennaAdminMixin.sortable_by + ('status', 'user')
    list_filter = AntennaAdminMixin.list_filter + ('status', 'user')
    readonly_fields = AntennaAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(AntennaTypeSuggestion)
class AntennaTypeSuggestionAdmin(BaseSuggestionAdminMixin, AntennaTypeAdminMixin):
    list_display = AntennaTypeAdminMixin.list_display + ('status', 'user')
    list_filter = AntennaTypeAdminMixin.list_filter + ('status', 'user')
    readonly_fields = ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(AntennaConnectorSuggestion)
class AntennaConnectorSuggestionAdmin(BaseSuggestionAdminMixin, AntennaConnectorAdminMixin):
    list_display = AntennaConnectorAdminMixin.list_display + ('status', 'user')
    list_filter = AntennaConnectorAdminMixin.list_filter + ('status', 'user')
    readonly_fields = ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingAntennaDetailSuggestion)
class ExistingAntennaDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'id', 'antenna', 'connector_type', 'status', 'user')
    list_filter = ('status', 'user', 'antenna', 'connector_type')
    readonly_fields = ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)