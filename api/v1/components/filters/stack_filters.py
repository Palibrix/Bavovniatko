from django_filters import rest_framework as filters

from components.models import FlightController, Stack, SpeedController, SpeedControllerProtocol, \
    SpeedControllerFirmware, FlightControllerFirmware


class StackFilter(filters.FilterSet):
    gyro__max_freq = filters.RangeFilter(field_name='flight_controller__gyro__max_freq')

    cont_current = filters.RangeFilter(field_name='speed_controller__cont_current')
    burst_current = filters.RangeFilter(field_name='speed_controller__burst_current')

    flight_controller_firmwares = filters.ModelMultipleChoiceFilter(
        field_name='flight_controller__firmwares__firmware',
        to_field_name='firmware',
        queryset=FlightControllerFirmware.objects.all(),
        conjoined=True,
    )

    speed_controller_protocols = filters.ModelMultipleChoiceFilter(
        field_name='speed_controller__protocols__protocol',
        to_field_name='protocol',
        queryset=SpeedControllerProtocol.objects.all(),
        conjoined=True,
    )

    speed_controller_firmwares = filters.ModelMultipleChoiceFilter(
        field_name='speed_controller__firmwares__firmware',
        to_field_name='firmware',
        queryset=SpeedControllerFirmware.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Stack
        fields = ['manufacturer', 'flight_controller__manufacturer', 'speed_controller__manufacturer',

                  'flight_controller', 'speed_controller',

                  'flight_controller__gyro__imu', 'flight_controller__gyro__spi_support',
                  'gyro__max_freq',
                  'flight_controller__bluetooth', 'flight_controller__wifi', 'flight_controller__barometer',
                  'flight_controller__voltage__min_cells', 'flight_controller__voltage__max_cells',
                  'flight_controller_firmwares',
                  'flight_controller__connector_type',
                  'flight_controller__mount_length', 'flight_controller__mount_width',

                  'speed_controller__is_wireless_conf', 'speed_controller__esc_type',
                  'speed_controller__voltage__min_cells', 'speed_controller__voltage__max_cells',
                  'cont_current', 'burst_current',
                  'speed_controller_firmwares', 'speed_controller_protocols',
                  'speed_controller__mount_length', 'speed_controller__mount_width',
                  ]


class FlightControllerFilter(filters.FilterSet):
    gyro__max_freq = filters.RangeFilter(field_name='gyro__max_freq')
    in_stack = filters.BooleanFilter(field_name='stack', lookup_expr='isnull', exclude=True)
    weight = filters.RangeFilter(field_name='weight')

    firmwares = filters.ModelMultipleChoiceFilter(
        field_name='firmwares__firmware',
        to_field_name='firmware',
        queryset=FlightControllerFirmware.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = FlightController
        fields = ['manufacturer',
                  'bluetooth', 'wifi', 'barometer',
                  'connector_type',
                  'mount_length', 'mount_width',

                  'gyro__imu', 'gyro__spi_support',
                  'gyro__max_freq',

                  'voltage__min_cells', 'voltage__max_cells',
                  'firmwares',

                  'in_stack', 'weight'
                  ]


class SpeedControllerFilter(filters.FilterSet):
    cont_current = filters.RangeFilter(field_name='cont_current')
    burst_current = filters.RangeFilter(field_name='burst_current')
    in_stack = filters.BooleanFilter(field_name='stack', lookup_expr='isnull', exclude=True)
    weight = filters.RangeFilter(field_name='weight')

    protocols = filters.ModelMultipleChoiceFilter(
        field_name='protocols__protocol',
        to_field_name='protocol',
        queryset=SpeedControllerProtocol.objects.all(),
        conjoined=True,  # This ensures that all selected protocols must be present
    )

    firmwares = filters.ModelMultipleChoiceFilter(
        field_name='firmwares__firmware',
        to_field_name='firmware',
        queryset=SpeedControllerFirmware.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = SpeedController
        fields = ['manufacturer',
                  'is_wireless_conf', 'esc_type',
                  'cont_current', 'burst_current',
                  'mount_length', 'mount_width',

                  'voltage__min_cells', 'voltage__max_cells',

                  'firmwares', 'protocols',

                  'in_stack', 'weight'
                  ]
