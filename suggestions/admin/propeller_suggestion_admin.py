from django.contrib import admin

from components.mixins.admin.base_propeller_admin_mixins import PropellerAdminMixin
from documents.admin.components_admin import PropellerDocumentInline
from galleries.admin.components_admin import PropellerGalleryInline
from suggestions.mixins import BaseSuggestionAdminMixin
from suggestions.models import PropellerSuggestion


@admin.register(PropellerSuggestion)
class PropellerSuggestionAdmin(BaseSuggestionAdminMixin, PropellerAdminMixin):
    inlines = [PropellerGalleryInline, PropellerDocumentInline]
    list_display = PropellerAdminMixin.list_display + ('status', 'user')
    list_filter = PropellerAdminMixin.list_filter + ('status', 'user')
    readonly_fields = PropellerAdminMixin.readonly_fields + ('related_instance', 'status')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
