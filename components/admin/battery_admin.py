from django.contrib import admin

from components.mixins import BaseModelAdminMixin
from components.models import Battery


@admin.register(Battery)
class BatteryAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'voltage', 'get_dimensions', 'discharge_current')
    exclude = ('model', )
    sortable_by = ('size', 'capacity')
    list_filter = ('size', 'type', 'discharge_current', 'connector_type')
