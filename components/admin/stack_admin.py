from django.contrib import admin

from components.mixins import BaseModelAdminMixin
from components.models import SpeedControllerProtocol, SpeedControllerFirmware, FlightControllerFirmware, Gyro, Stack, \
    FlightController, SpeedController


@admin.register(Stack)
class StackAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'flight_controller', 'speed_controller',)
    list_filter = ('flight_controller', 'speed_controller')
    search_fields = ('manufacturer', 'model', 'id')


@admin.register(FlightController)
class FlightControllerAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'voltage', 'connector_type',
                    'get_dimensions', 'get_mount_dimensions',
                    'bluetooth', 'wifi', 'barometer',
                    'weight')
    list_filter = ('model', 'voltage', 'connector_type',
                   'bluetooth', 'wifi', 'barometer')
    search_fields = ('manufacturer', 'model', 'id')
    sortable_by = ('weight', )


@admin.register(SpeedController)
class SpeedControllerAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',
                    'voltage', 'get_burst_current',
                    'get_dimensions', 'get_mount_dimensions',
                    'is_wireless_conf',
                    'weight')
    list_filter = ('model', 'voltage', 'esc_type', 'is_wireless_conf',)
    search_fields = ('manufacturer', 'model', 'id')
    sortable_by = ('weight',)


@admin.register(Gyro)
class GyroAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'spi_support')
    list_filter = ('spi_support',)
    search_fields = ('manufacturer', 'imu')
    sortable_by = ('max_freq',)


@admin.register(FlightControllerFirmware)
class FlightControllerFirmwareAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('firmware', )


@admin.register(SpeedControllerFirmware)
class SpeedControllerFirmwareAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('firmware', )


@admin.register(SpeedControllerProtocol)
class SpeedControllerProtocolAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('protocol',)
