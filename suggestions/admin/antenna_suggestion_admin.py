from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.base_antenna_admin_mixins import AntennaAdminMixin
from documents.admin.components_admin import AntennaDocumentInline
from galleries.admin.components_admin import AntennaGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_suggestions import ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion


class SuggestedAntennaDetailSuggestionInline(admin.StackedInline):
    model = SuggestedAntennaDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'antenna'


@admin.register(AntennaSuggestion)
class AntennaSuggestionAdmin(BaseSuggestionAdminMixin, AntennaAdminMixin):
    inlines = [SuggestedAntennaDetailSuggestionInline, AntennaGalleryInline, AntennaDocumentInline]
    list_display = AntennaAdminMixin.list_display + ('reviewed', 'accepted', 'user')
    sortable_by = AntennaAdminMixin.sortable_by + ('reviewed', 'accepted', 'user')
    list_filter = AntennaAdminMixin.list_filter + ('reviewed', 'accepted', 'user')
    readonly_fields = AntennaAdminMixin.readonly_fields + ('related_instance', "reviewed", 'accepted')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingAntennaDetailSuggestion)
class ExistingAntennaDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'id', 'reviewed', 'accepted', 'user')
    sortable_by = ('antenna', 'reviewed', 'accepted', 'user')
    list_filter = ('reviewed', 'accepted', 'user')
    readonly_fields = ('related_instance', "reviewed", 'accepted')
