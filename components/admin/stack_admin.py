from django.contrib import admin

from components.admin import IsPublicFilter
from components.mixins import IsPublicMixin
from components.models import SpeedControllerProtocol, SpeedControllerFirmware, FlightControllerFirmware, Gyro, Stack, \
    FlightController, SpeedController

admin.site.register(SpeedControllerProtocol)
admin.site.register(SpeedControllerFirmware)
admin.site.register(FlightControllerFirmware)
admin.site.register(Gyro)


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('__str__', 'flight_controller', 'speed_controller', 'is_public')
    list_filter = ('flight_controller', 'speed_controller', IsPublicFilter)
    search_fields = ('model', 'id')


@admin.register(FlightController)
class FlightControllerAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'id', 'voltage', 'connector_type', 'get_params', 'get_mount_params', 'is_public')
    list_filter = ('model', 'voltage', 'connector_type', IsPublicFilter)
    search_fields = ('model', 'id')


@admin.register(SpeedController)
class SpeedControllerAdmin(admin.ModelAdmin, IsPublicMixin):
    list_display = ('model', 'id', 'voltage', 'get_cont_current', 'get_burst_current',
                    'get_params', 'get_mount_params', 'is_public')
    list_filter = ('model', 'voltage', IsPublicFilter)
    search_fields = ('model', 'id')
