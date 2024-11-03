from django_filters import rest_framework as filters

from components.models import OutputPower, Transmitter, VideoFormat, AntennaConnector


class TransmitterFilter(filters.FilterSet):
    output_voltage = filters.RangeFilter(field_name='output_voltage')
    channels_quantity = filters.RangeFilter(field_name='channels_quantity')
    max_power = filters.RangeFilter(field_name='max_power')
    weight = filters.RangeFilter(field_name='weight')

    output_powers = filters.ModelMultipleChoiceFilter(
        field_name='output_powers__output_power',
        to_field_name='output_power',
        queryset=OutputPower.objects.all(),
        conjoined=True,
    )
    formats = filters.ModelMultipleChoiceFilter(
        field_name='video_formats__format',
        to_field_name='format',
        queryset=VideoFormat.objects.all(),
        conjoined=True,
    )
    antenna_connectors = filters.ModelMultipleChoiceFilter(
        field_name='antenna_connectors__type',
        to_field_name='type',
        queryset=AntennaConnector.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Transmitter
        fields = ['manufacturer', 'input_voltage_min', 'input_voltage_max', 'output_voltage',
                  'channels_quantity', 'output', 'max_power', 'microphone',
                  'output_powers', 'antenna_connectors', 'formats',
                  'weight']
