from components.mixins import BaseModelAdminMixin


class StackAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'flight_controller', 'speed_controller',)
    list_filter = ('flight_controller', 'speed_controller')
    search_fields = ('manufacturer', 'model', 'id')


class FlightControllerAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'voltage', 'connector_type',
                    'get_dimensions', 'get_mount_dimensions',
                    'bluetooth', 'wifi', 'barometer',
                    'weight')
    list_filter = ('model', 'voltage', 'connector_type',
                   'bluetooth', 'wifi', 'barometer')
    search_fields = ('manufacturer', 'model', 'id')
    sortable_by = ('weight', )


class SpeedControllerAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',
                    'voltage', 'get_burst_current',
                    'get_dimensions', 'get_mount_dimensions',
                    'is_wireless_conf',
                    'weight')
    list_filter = ('model', 'voltage', 'esc_type', 'is_wireless_conf',)
    search_fields = ('manufacturer', 'model', 'id')
    sortable_by = ('weight',)


class GyroAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'spi_support')
    list_filter = ('spi_support',)
    search_fields = ('manufacturer', 'imu')
    sortable_by = ('max_freq',)


class FlightControllerFirmwareAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('firmware', )


class SpeedControllerFirmwareAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('firmware', )


class SpeedControllerProtocolAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id',)
    search_fields = ('protocol',)