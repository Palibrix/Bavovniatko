from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Propeller


class PropellerFilter(MetadataFilterSet):
    """
    Filter for Propellers with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    size_min = filters.NumberFilter(field_name='size', lookup_expr='gte')
    size_max = filters.NumberFilter(field_name='size', lookup_expr='lte')

    pitch_min = filters.NumberFilter(field_name='pitch', lookup_expr='gte')
    pitch_max = filters.NumberFilter(field_name='pitch', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    # Choice filters
    blade_count = filters.CharFilter(field_name='blade_count')

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
                "id": "dimensions",
                "title": "Propeller Dimensions",
                "filters": [
                    {
                        "id": "size",
                        "type": "range",
                        "label": "Size",
                        "field": "size",
                        "unit": "\"",
                        "default_value": 5
                    },
                    {
                        "id": "pitch",
                        "type": "range",
                        "label": "Pitch",
                        "field": "pitch",
                        "unit": "\"",
                        "default_value": 4.5
                    }
                ]
            },
            {
                "id": "configuration",
                "title": "Configuration",
                "filters": [
                    {
                        "id": "blade_count",
                        "type": "choice",
                        "label": "Blade Count",
                        "field": "blade_count"
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
                        "default_value": 5
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Propeller
        fields = [
            'manufacturer',
            'size_min', 'size_max',
            'pitch_min', 'pitch_max',
            'blade_count',
            'weight_min', 'weight_max'
        ]