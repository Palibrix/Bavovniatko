from django.contrib import admin

from components.mixins import BaseModelAdminMixin
from components.models import Propeller
from documents.admin.components_admin import PropellerDocumentInline
from galleries.admin.components_admin import PropellerGalleryInline


@admin.register(Propeller)
class PropellerAdmin(BaseModelAdminMixin):
    inlines = [PropellerGalleryInline, PropellerDocumentInline]
    list_display = ('__str__', 'id', 'size', 'pitch', 'blade_count')
    list_filter = ('manufacturer', 'blade_count', 'weight')
    search_fields = ('manufacturer', 'model', 'id', 'size', 'pitch',)
    sortable_by = ('manufacturer', 'weight')
