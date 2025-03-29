from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Receiver, AntennaConnector, ReceiverProtocolType


class ReceiverFilter(MetadataFilterSet):
    """
    Filter for Receivers with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    frequency_min = filters.NumberFilter(field_name='details__frequency', lookup_expr='gte')
    frequency_max = filters.NumberFilter(field_name='details__frequency', lookup_expr='lte')

    telemetry_power_min = filters.NumberFilter(field_name='details__telemetry_power', lookup_expr='gte')
    telemetry_power_max = filters.NumberFilter(field_name='details__telemetry_power', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='details__weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='details__weight', lookup_expr='lte')

    voltage_min = filters.NumberFilter(field_name='voltage_min', lookup_expr='gte')
    voltage_max = filters.NumberFilter(field_name='voltage_max', lookup_expr='lte')

    # Choice filters
    processor = filters.CharFilter(field_name='processor')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')

    antenna_connectors = filters.ModelMultipleChoiceFilter(
        field_name='antenna_connectors__type',
        to_field_name='type',
        queryset=AntennaConnector.objects.all(),
        conjoined=True,
    )

    protocols = filters.ModelMultipleChoiceFilter(
        field_name='protocols__type',
        to_field_name='type',
        queryset=ReceiverProtocolType.objects.all(),
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
                "id": "technical",
                "title": "Technical Specifications",
                "filters": [
                    {
                        "id": "processor",
                        "type": "choice",
                        "label": "Processor",
                        "field": "processor"
                    },
                    {
                        "id": "frequency",
                        "type": "range",
                        "label": "Frequency",
                        "field": "details__frequency",
                        "unit": "MHz",
                        "default_value": 2400
                    },
                    {
                        "id": "telemetry_power",
                        "type": "range",
                        "label": "Telemetry Power",
                        "field": "details__telemetry_power",
                        "unit": "mW",
                        "default_value": 25
                    },
                    {
                        "id": "voltage",
                        "type": "range",
                        "label": "Voltage",
                        "field": "voltage_min",
                        "unit": "V",
                        "default_value": 5
                    }
                ]
            },
            {
                "id": "connectors",
                "title": "Connectors & Protocols",
                "filters": [
                    {
                        "id": "antenna_connectors",
                        "type": "choice",
                        "label": "Antenna Connectors",
                        "field": "antenna_connectors__type",
                        "model_field": "type"
                    },
                    {
                        "id": "protocols",
                        "type": "choice",
                        "label": "Protocols",
                        "field": "protocols__type",
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
                        "field": "details__weight",
                        "unit": "g",
                        "default_value": 5
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Receiver
        fields = [
            'manufacturer',
            'processor',
            'frequency_min', 'frequency_max',
            'telemetry_power_min', 'telemetry_power_max',
            'weight_min', 'weight_max',
            'voltage_min', 'voltage_max',
            'antenna_connectors',
            'protocols'
        ]