from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_receiver_admin_mixins import (
    ReceiverAdminMixin, ReceiverProtocolTypeAdminMixin
)
from documents.admin.components_admin import ReceiverDocumentInline
from galleries.admin.components_admin import ReceiverGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import (
    ReceiverSuggestion, ReceiverProtocolTypeSuggestion, 
    ExistingReceiverDetailSuggestion, SuggestedReceiverDetailSuggestion
)


class SuggestedReceiverDetailInline(admin.StackedInline):
    model = SuggestedReceiverDetailSuggestion
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'suggestion'


@admin.register(ReceiverSuggestion)
class ReceiverSuggestionAdmin(BaseSuggestionAdminMixin, ReceiverAdminMixin):
    inlines = [SuggestedReceiverDetailInline, ReceiverGalleryInline, ReceiverDocumentInline]
    list_display = ReceiverAdminMixin.list_display + ('status', 'user')
    list_filter = ReceiverAdminMixin.list_filter + ('status', 'user')
    readonly_fields = ReceiverAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReceiverProtocolTypeSuggestion)
class ReceiverProtocolTypeSuggestionAdmin(BaseSuggestionAdminMixin, ReceiverProtocolTypeAdminMixin):
    list_display = ReceiverProtocolTypeAdminMixin.list_display + ('status', 'user')
    list_filter = ('status', 'user')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExistingReceiverDetailSuggestion)
class ExistingReceiverDetailSuggestionAdmin(BaseSuggestionAdminMixin):
    list_display = ('__str__', 'receiver', 'status', 'user')
    list_filter = ('status', 'user', 'receiver')
    readonly_fields = ('related_instance', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
