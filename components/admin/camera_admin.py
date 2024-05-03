from django.contrib import admin

from .filters import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'manufacturer', 'id', 'tvl', 'light_sens', 'ratio', 'user', 'is_public')
    list_filter = ('manufacturer', 'light_sens', 'output_type', 'ratio', IsPublicFilter)
    search_fields = ('model', 'manufacturer', 'id', 'tvl')
