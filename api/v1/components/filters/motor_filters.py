from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Motor, RatedVoltage


class MotorFilter(MetadataFilterSet):
    """
    Filter for Motors with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    max_power_min = filters.NumberFilter(field_name='details__max_power', lookup_expr='gte')
    max_power_max = filters.NumberFilter(field_name='details__max_power', lookup_expr='lte')

    kv_per_volt_min = filters.NumberFilter(field_name='details__kv_per_volt', lookup_expr='gte')
    kv_per_volt_max = filters.NumberFilter(field_name='details__kv_per_volt', lookup_expr='lte')

    peak_current_min = filters.NumberFilter(field_name='details__peak_current', lookup_expr='gte')
    peak_current_max = filters.NumberFilter(field_name='details__peak_current', lookup_expr='lte')

    idle_current_min = filters.NumberFilter(field_name='details__idle_current', lookup_expr='gte')
    idle_current_max = filters.NumberFilter(field_name='details__idle_current', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='details__weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='details__weight', lookup_expr='lte')

    stator_diameter_min = filters.NumberFilter(field_name='stator_diameter', lookup_expr='gte')
    stator_diameter_max = filters.NumberFilter(field_name='stator_diameter', lookup_expr='lte')

    stator_height_min = filters.NumberFilter(field_name='stator_height', lookup_expr='gte')
    stator_height_max = filters.NumberFilter(field_name='stator_height', lookup_expr='lte')

    # Choice filters
    configuration = filters.CharFilter(field_name='configuration')
    voltage_type = filters.CharFilter(field_name='details__voltage__type')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')
    min_cells = filters.BaseInFilter(field_name='details__voltage__min_cells')
    max_cells = filters.BaseInFilter(field_name='details__voltage__max_cells')

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
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "stator_diameter",
                        "type": "range",
                        "label": "Stator Diameter",
                        "field": "stator_diameter",
                        "unit": "mm",
                        "default_value": 22
                    },
                    {
                        "id": "stator_height",
                        "type": "range",
                        "label": "Stator Height",
                        "field": "stator_height",
                        "unit": "mm",
                        "default_value": 7
                    },
                    {
                        "id": "configuration",
                        "type": "choice",
                        "label": "Configuration",
                        "field": "configuration"
                    },
                    {
                        "id": "weight",
                        "type": "range",
                        "label": "Weight",
                        "field": "details__weight",
                        "unit": "g",
                        "default_value": 30
                    }
                ]
            },
            {
                "id": "performance",
                "title": "Performance Characteristics",
                "filters": [
                    {
                        "id": "kv_per_volt",
                        "type": "range",
                        "label": "KV Rating",
                        "field": "details__kv_per_volt",
                        "unit": "KV",
                        "default_value": 2300
                    },
                    {
                        "id": "max_power",
                        "type": "range",
                        "label": "Max Power",
                        "field": "details__max_power",
                        "unit": "W",
                        "default_value": 350
                    },
                    {
                        "id": "peak_current",
                        "type": "range",
                        "label": "Peak Current",
                        "field": "details__peak_current",
                        "unit": "A",
                        "default_value": 35
                    },
                    {
                        "id": "idle_current",
                        "type": "range",
                        "label": "Idle Current",
                        "field": "details__idle_current",
                        "unit": "A",
                        "default_value": 0.5
                    }
                ]
            },
            {
                "id": "power",
                "title": "Power Requirements",
                "filters": [
                    {
                        "id": "voltage_type",
                        "type": "choice",
                        "label": "Voltage Type",
                        "field": "details__voltage__type"
                    },
                    {
                        "id": "min_cells",
                        "type": "choice",
                        "label": "Min. Cells",
                        "field": "details__voltage__min_cells"
                    },
                    {
                        "id": "max_cells",
                        "type": "choice",
                        "label": "Max. Cells",
                        "field": "details__voltage__max_cells"
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Motor
        fields = [
            'manufacturer',
            'stator_diameter_min', 'stator_diameter_max',
            'stator_height_min', 'stator_height_max',
            'configuration',
            'max_power_min', 'max_power_max',
            'kv_per_volt_min', 'kv_per_volt_max',
            'peak_current_min', 'peak_current_max',
            'idle_current_min', 'idle_current_max',
            'min_cells', 'max_cells',
            'voltage_type',
            'weight_min', 'weight_max'
        ]
