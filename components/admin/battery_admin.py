from django.contrib import admin

from components.mixins.admin.base_battery_admin_mixins import BatteryAdminMixin
from components.models import Battery


@admin.register(Battery)
class BatteryAdmin(BatteryAdminMixin):
    pass