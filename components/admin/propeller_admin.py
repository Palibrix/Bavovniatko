from django.contrib import admin

from .filters import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import Propeller


@admin.register(Propeller)
class PropellerAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'id', 'size', 'pitch', 'blade_count', 'user', 'is_public')
    list_filter = ('manufacturer', 'blade_count', IsPublicFilter)
    search_fields = ('model', 'id', 'size', 'pitch', 'blade_count')
    