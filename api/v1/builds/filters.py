from django_filters import rest_framework as filters

from builds.models import Drone
from components.models import Antenna, AntennaConnector, VideoFormat, ReceiverProtocolType


class DroneFilter(filters.FilterSet):
    antenna__center_frequency = filters.RangeFilter(field_name='antenna__center_frequency')
    antenna__swr = filters.RangeFilter(field_name='antenna__swr', )
    antenna__gain = filters.RangeFilter(field_name='antenna__gain')
    antenna__radiation = filters.RangeFilter(field_name='antenna__radiation')

    battery__series = filters.RangeFilter(field_name='battery__series')
    battery__parallels = filters.RangeFilter(field_name='battery__parallels')
    battery__voltage = filters.RangeFilter(field_name='battery__voltage')

    camera__fov = filters.RangeFilter(field_name='fov')
    camera__formats = filters.ModelMultipleChoiceFilter(
        field_name='camera__video_formats__format',
        to_field_name='format',
        queryset=VideoFormat.objects.all(),
        conjoined=True,
    )

    motor__max_power = filters.RangeFilter(field_name='motor__details__max_power')
    motor__kv_per_volt = filters.RangeFilter(field_name='motor__details__kv_per_volt')

    receiver__frequency = filters.RangeFilter(field_name='receiver__details__frequency')
    receiver__telemetry_power = filters.RangeFilter(field_name='receiver__details__telemetry_power')
    receiver__protocols = filters.ModelMultipleChoiceFilter(
        field_name='receiver__protocols__type',
        to_field_name='type',
        queryset=ReceiverProtocolType.objects.all(),
        conjoined=True,
    )

    transmitter__channels_quantity = filters.RangeFilter(field_name='transmitter__channels_quantity')
    transmitter__max_power = filters.RangeFilter(field_name='transmitter__max_power')
    transmitter__formats = filters.ModelMultipleChoiceFilter(
        field_name='video_formats__format',
        to_field_name='format',
        queryset=VideoFormat.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Drone
        fields = ['manufacturer', 'type',
                  'antenna', 'camera', 'frame', 'motor', 'propeller',
                  'receiver', 'transmitter', 'flight_controller', 'speed_controller',

                  'antenna__center_frequency', 'antenna__swr', 'antenna__gain', 'antenna__radiation',
                  'antenna__type__type', 'antenna__type__direction', 'antenna__type__polarization',
                  'antenna__details__angle_type',

                  'battery__series', 'battery__parallels', 'battery__size', 'battery__type',
                  'battery__capacity', 'battery__voltage',

                  'camera__ratio', 'camera__output_type', 'camera__formats', 'camera__light_sens',
                  'camera__fov',

                  'motor__max_power', 'motor__kv_per_volt',

                  'receiver__frequency', 'receiver__telemetry_power', 'receiver__protocols',

                  'flight_controller__gyro__spi_support',
                  'flight_controller__bluetooth', 'flight_controller__wifi', 'flight_controller__barometer',

                  'speed_controller__is_wireless_conf', 'speed_controller__esc_type',

                  'transmitter__channels_quantity', 'transmitter__output', 'transmitter__max_power',
                  'transmitter__microphone', 'transmitter__formats',

                  ]
