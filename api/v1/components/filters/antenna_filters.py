from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Antenna, AntennaConnector


class AntennaFilter(MetadataFilterSet):
    """
    Filter for Antennas with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    center_frequency_min = filters.NumberFilter(field_name='center_frequency', lookup_expr='gte')
    center_frequency_max = filters.NumberFilter(field_name='center_frequency', lookup_expr='lte')

    swr_min = filters.NumberFilter(field_name='swr', lookup_expr='gte')
    swr_max = filters.NumberFilter(field_name='swr', lookup_expr='lte')

    gain_min = filters.NumberFilter(field_name='gain', lookup_expr='gte')
    gain_max = filters.NumberFilter(field_name='gain', lookup_expr='lte')

    radiation_min = filters.NumberFilter(field_name='radiation', lookup_expr='gte')
    radiation_max = filters.NumberFilter(field_name='radiation', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='details__weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='details__weight', lookup_expr='lte')

    # Choice filters
    type = filters.CharFilter(field_name='type__type')
    direction = filters.CharFilter(field_name='type__direction')
    polarization = filters.CharFilter(field_name='type__polarization')
    connector_type = filters.CharFilter(field_name='details__connector_type__type')
    angle_type = filters.CharFilter(field_name='details__angle_type')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')

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
                        "id": "center_frequency",
                        "type": "range",
                        "label": "Center Frequency",
                        "field": "center_frequency",
                        "unit": "MHz",
                        "default_value": 3000
                    },
                    {
                        "id": "swr",
                        "type": "range",
                        "label": "SWR (VSWR)",
                        "field": "swr",
                        "default_value": 2
                    },
                    {
                        "id": "gain",
                        "type": "range",
                        "label": "Gain",
                        "field": "gain",
                        "unit": "dBi",
                        "default_value": 2.5
                    },
                    {
                        "id": "radiation",
                        "type": "range",
                        "label": "Radiation Efficiency",
                        "field": "radiation",
                        "unit": "%",
                        "default_value": 50
                    }
                ]
            },
            {
                "id": "antenna_type",
                "title": "Antenna Type",
                "filters": [
                    {
                        "id": "direction",
                        "type": "choice",
                        "label": "Direction",
                        "field": "type__direction"
                    },
                    {
                        "id": "polarization",
                        "type": "choice",
                        "label": "Polarization",
                        "field": "type__polarization"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "connector_type",
                        "type": "choice",
                        "label": "Connector Type",
                        "field": "details__connector_type__type",
                        "model_field": "type"
                    },
                    {
                        "id": "angle_type",
                        "type": "choice",
                        "label": "Angle Type",
                        "field": "details__angle_type"
                    },
                    {
                        "id": "weight",
                        "type": "range",
                        "label": "Weight",
                        "field": "details__weight",
                        "unit": "g",
                        "default_value": 15
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Antenna
        fields = [
            'manufacturer',
            'center_frequency_min', 'center_frequency_max',
            'swr_min', 'swr_max',
            'gain_min', 'gain_max',
            'radiation_min', 'radiation_max',
            'direction', 'polarization',
            'connector_type', 'angle_type',
            'weight_min', 'weight_max'
        ]