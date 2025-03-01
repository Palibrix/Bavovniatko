from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_camera_admin_mixins import CameraAdminMixin, VideoFormatAdminMixin
from documents.admin.components_admin import CameraDocumentInline
from galleries.admin.components_admin import CameraGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    CameraSuggestion, VideoFormatSuggestion, ExistingCameraDetailSuggestion,
    SuggestedCameraDetailSuggestion
)


class SuggestedCameraDetailSuggestionInline(admin.StackedInline):
    model = SuggestedCameraDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


@admin.register(CameraSuggestion)
class CameraSuggestionAdmin(BaseSuggestionAdminMixin, CameraAdminMixin):
    inlines = [SuggestedCameraDetailSuggestionInline, CameraGalleryInline, CameraDocumentInline]
    list_display = CameraAdminMixin.list_display + ('status', 'user')
    list_filter = CameraAdminMixin.list_filter + ('status', 'user')
    readonly_fields = CameraAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(VideoFormatSuggestion)
class VideoFormatSuggestionAdmin(BaseSuggestionAdminMixin, VideoFormatAdminMixin):
    list_display = VideoFormatAdminMixin.list_display + ('status', 'user')
    list_filter = VideoFormatAdminMixin.list_filter + ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingCameraDetailSuggestion)
class ExistingCameraDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'camera', 'status', 'user')
    list_filter = ('status', 'user', 'camera')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
