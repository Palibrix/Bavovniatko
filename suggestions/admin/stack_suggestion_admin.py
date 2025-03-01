from django.contrib import admin

from components.mixins.admin.base_stack_admin_mixins import (
    StackAdminMixin, FlightControllerAdminMixin, SpeedControllerAdminMixin,
    GyroAdminMixin, FlightControllerFirmwareAdminMixin, 
    SpeedControllerFirmwareAdminMixin, SpeedControllerProtocolAdminMixin
)
from documents.admin.components_admin import (
    StackDocumentInline, FlightControllerDocumentInline, SpeedControllerDocumentInline
)
from galleries.admin.components_admin import (
    StackGalleryInline, FlightControllerGalleryInline, SpeedControllerGalleryInline
)
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    StackSuggestion, FlightControllerSuggestion, SpeedControllerSuggestion,
    GyroSuggestion, FlightControllerFirmwareSuggestion,
    SpeedControllerFirmwareSuggestion, SpeedControllerProtocolSuggestion
)


@admin.register(StackSuggestion)
class StackSuggestionAdmin(BaseSuggestionAdminMixin, StackAdminMixin):
    inlines = [StackGalleryInline, StackDocumentInline]
    list_display = StackAdminMixin.list_display + ('status', 'user')
    list_filter = StackAdminMixin.list_filter + ('status', 'user')
    readonly_fields = StackAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(FlightControllerSuggestion)
class FlightControllerSuggestionAdmin(BaseSuggestionAdminMixin, FlightControllerAdminMixin):
    inlines = [FlightControllerGalleryInline, FlightControllerDocumentInline]
    list_display = FlightControllerAdminMixin.list_display + ('status', 'user')
    list_filter = FlightControllerAdminMixin.list_filter + ('status', 'user')
    readonly_fields = FlightControllerAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(SpeedControllerSuggestion)
class SpeedControllerSuggestionAdmin(BaseSuggestionAdminMixin, SpeedControllerAdminMixin):
    inlines = [SpeedControllerGalleryInline, SpeedControllerDocumentInline]
    list_display = SpeedControllerAdminMixin.list_display + ('status', 'user')
    list_filter = SpeedControllerAdminMixin.list_filter + ('status', 'user')
    readonly_fields = SpeedControllerAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(GyroSuggestion)
class GyroSuggestionAdmin(BaseSuggestionAdminMixin, GyroAdminMixin):
    list_display = GyroAdminMixin.list_display + ('status', 'user')
    list_filter = GyroAdminMixin.list_filter + ('status', 'user')
    readonly_fields = GyroAdminMixin.readonly_fields + ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(FlightControllerFirmwareSuggestion)
class FlightControllerFirmwareSuggestionAdmin(BaseSuggestionAdminMixin, FlightControllerFirmwareAdminMixin):
    list_display = FlightControllerFirmwareAdminMixin.list_display + ('status', 'user')
    list_filter = ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(SpeedControllerFirmwareSuggestion)
class SpeedControllerFirmwareSuggestionAdmin(BaseSuggestionAdminMixin, SpeedControllerFirmwareAdminMixin):
    list_display = SpeedControllerFirmwareAdminMixin.list_display + ('status', 'user')
    list_filter = ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(SpeedControllerProtocolSuggestion)
class SpeedControllerProtocolSuggestionAdmin(BaseSuggestionAdminMixin, SpeedControllerProtocolAdminMixin):
    list_display = SpeedControllerProtocolAdminMixin.list_display + ('status', 'user')
    list_filter = ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
