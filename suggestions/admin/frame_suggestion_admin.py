from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_frame_admin_mixins import FrameAdminMixin
from documents.admin.components_admin import FrameDocumentInline
from galleries.admin.components_admin import FrameGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    FrameSuggestion, ExistingFrameCameraDetailSuggestion, 
    ExistingFrameMotorDetailSuggestion, ExistingFrameVTXDetailSuggestion,
    SuggestedFrameCameraDetailSuggestion, SuggestedFrameMotorDetailSuggestion, 
    SuggestedFrameVTXDetailSuggestion
)


class SuggestedFrameCameraDetailInline(admin.StackedInline):
    model = SuggestedFrameCameraDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


class SuggestedFrameMotorDetailInline(admin.StackedInline):
    model = SuggestedFrameMotorDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


class SuggestedFrameVTXDetailInline(admin.StackedInline):
    model = SuggestedFrameVTXDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


@admin.register(FrameSuggestion)
class FrameSuggestionAdmin(BaseSuggestionAdminMixin, FrameAdminMixin):
    inlines = [
        SuggestedFrameCameraDetailInline, 
        SuggestedFrameMotorDetailInline, 
        SuggestedFrameVTXDetailInline,
        FrameGalleryInline, 
        FrameDocumentInline
    ]
    list_display = FrameAdminMixin.list_display + ('status', 'user')
    list_filter = FrameAdminMixin.list_filter + ('status', 'user')
    readonly_fields = FrameAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingFrameCameraDetailSuggestion)
class ExistingFrameCameraDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'frame', 'status', 'user')
    list_filter = ('status', 'user', 'frame')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingFrameMotorDetailSuggestion)
class ExistingFrameMotorDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'frame', 'status', 'user')
    list_filter = ('status', 'user', 'frame')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingFrameVTXDetailSuggestion)
class ExistingFrameVTXDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'frame', 'status', 'user')
    list_filter = ('status', 'user', 'frame')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
