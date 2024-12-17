from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from builds.forms import RequiredInlineFormSet
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_requests import ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion


class SuggestedAntennaDetailSuggestionInline(admin.StackedInline):
    model = SuggestedAntennaDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'antenna'


class AntennaSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'id', 'type', 'reviewed', 'accepted')
    sortable_by = ('swr', 'radiation', 'reviewed')
    list_filter = ('manufacturer', 'model', 'reviewed')
    search_fields = ('manufacturer', 'model', 'id',)
    inlines = [SuggestedAntennaDetailSuggestionInline]
    readonly_fields = ('related_instance' ,"reviewed", 'accepted')

class ExistingAntennaDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'id', 'reviewed', 'accepted')

admin.site.register(AntennaSuggestion, AntennaSuggestionAdmin)
admin.site.register(ExistingAntennaDetailSuggestion, ExistingAntennaDetailSuggestionAdmin)