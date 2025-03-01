from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_motor_admin_mixins import MotorAdminMixin, RatedVoltageAdminMixin
from documents.admin.components_admin import MotorDocumentInline
from galleries.admin.components_admin import MotorGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    MotorSuggestion, RatedVoltageSuggestion, ExistingMotorDetailSuggestion,
    SuggestedMotorDetailSuggestion
)


class SuggestedMotorDetailInline(admin.StackedInline):
    model = SuggestedMotorDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


@admin.register(MotorSuggestion)
class MotorSuggestionAdmin(BaseSuggestionAdminMixin, MotorAdminMixin):
    inlines = [SuggestedMotorDetailInline, MotorGalleryInline, MotorDocumentInline]
    list_display = MotorAdminMixin.list_display + ('status', 'user')
    list_filter = MotorAdminMixin.list_filter + ('status', 'user')
    readonly_fields = MotorAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(RatedVoltageSuggestion)
class RatedVoltageSuggestionAdmin(BaseSuggestionAdminMixin, RatedVoltageAdminMixin):
    list_display = RatedVoltageAdminMixin.list_display + ('status', 'user')
    list_filter = RatedVoltageAdminMixin.list_filter + ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingMotorDetailSuggestion)
class ExistingMotorDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'motor', 'status', 'user')
    list_filter = ('status', 'user', 'motor')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
