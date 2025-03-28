from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Transmitter, OutputPower, VideoFormat, AntennaConnector


class TransmitterFilter(MetadataFilterSet):
    """
    Filter for Transmitters with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    output_voltage_min = filters.NumberFilter(field_name='output_voltage', lookup_expr='gte')
    output_voltage_max = filters.NumberFilter(field_name='output_voltage', lookup_expr='lte')

    channels_quantity_min = filters.NumberFilter(field_name='channels_quantity', lookup_expr='gte')
    channels_quantity_max = filters.NumberFilter(field_name='channels_quantity', lookup_expr='lte')

    max_power_min = filters.NumberFilter(field_name='max_power', lookup_expr='gte')
    max_power_max = filters.NumberFilter(field_name='max_power', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    input_voltage_min = filters.NumberFilter(field_name='input_voltage_min', lookup_expr='gte')
    input_voltage_max = filters.NumberFilter(field_name='input_voltage_max', lookup_expr='lte')

    # Choice filters
    output = filters.CharFilter(field_name='output')
    microphone = filters.BooleanFilter(field_name='microphone')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')

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

    # Define UI metadata for the filters
    filter_metadata = {
        "groups": [
            {
                "id": "manufacturer",
                "title": "Manufacturer",
                "filters": [
                    {
                        "id": "manufacturer",
                        "type": "choice",
                        "label": "Manufacturer",
                        "field": "manufacturer",
                        "searchable": True,
                    }
                ]
            },
            {
                "id": "power",
                "title": "Power & Output",
                "filters": [
                    {
                        "id": "input_voltage",
                        "type": "range",
                        "label": "Input Voltage",
                        "field": "input_voltage_min",
                        "unit": "V",
                        "default_value": 12
                    },
                    {
                        "id": "output_voltage",
                        "type": "range",
                        "label": "Output Voltage",
                        "field": "output_voltage",
                        "unit": "V",
                        "default_value": 5
                    },
                    {
                        "id": "max_power",
                        "type": "range",
                        "label": "Max Power",
                        "field": "max_power",
                        "unit": "mW",
                        "default_value": 600
                    },
                    {
                        "id": "output_powers",
                        "type": "choice",
                        "label": "Output Power Levels",
                        "field": "output_powers__output_power",
                        "model_field": "output_power"
                    }
                ]
            },
            {
                "id": "video",
                "title": "Video Configuration",
                "filters": [
                    {
                        "id": "channels_quantity",
                        "type": "range",
                        "label": "Channel Quantity",
                        "field": "channels_quantity",
                        "default_value": 40
                    },
                    {
                        "id": "output",
                        "type": "choice",
                        "label": "Output Type",
                        "field": "output"
                    },
                    {
                        "id": "formats",
                        "type": "choice",
                        "label": "Video Formats",
                        "field": "video_formats__format",
                        "model_field": "format"
                    },
                    {
                        "id": "microphone",
                        "type": "boolean",
                        "label": "Has Microphone",
                        "field": "microphone"
                    }
                ]
            },
            {
                "id": "connectors",
                "title": "Connections",
                "filters": [
                    {
                        "id": "antenna_connectors",
                        "type": "choice",
                        "label": "Antenna Connectors",
                        "field": "antenna_connectors__type",
                        "model_field": "type"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "weight",
                        "type": "range",
                        "label": "Weight",
                        "field": "weight",
                        "unit": "g",
                        "default_value": 15
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Transmitter
        fields = [
            'manufacturer',
            'input_voltage_min', 'input_voltage_max',
            'output_voltage_min', 'output_voltage_max',
            'channels_quantity_min', 'channels_quantity_max',
            'output',
            'max_power_min', 'max_power_max',
            'microphone',
            'output_powers',
            'antenna_connectors',
            'formats',
            'weight_min', 'weight_max'
        ]