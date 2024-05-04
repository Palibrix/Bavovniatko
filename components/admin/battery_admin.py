from django.contrib import admin

from components.mixins import IsPublicMixin
from components.models import Battery


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('configuration', 'size', 'type', 'capacity', 'voltage', 'discharge_current',
                    'get_params', 'is_public')
    sortable_by = ('configuration', 'size', 'capacity')
    list_filter = ('configuration', 'size', 'type', 'discharge_current')
