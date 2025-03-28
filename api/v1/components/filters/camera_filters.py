from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import VideoFormat, Camera


class CameraFilter(MetadataFilterSet):
    """
    Filter for Cameras with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    fov_min = filters.NumberFilter(field_name='fov', lookup_expr='gte')
    fov_max = filters.NumberFilter(field_name='fov', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    voltage_min = filters.NumberFilter(field_name='voltage_min', lookup_expr='gte')
    voltage_max = filters.NumberFilter(field_name='voltage_max', lookup_expr='lte')

    tvl_min = filters.NumberFilter(field_name='tvl', lookup_expr='gte')
    tvl_max = filters.NumberFilter(field_name='tvl', lookup_expr='lte')

    # Choice filters
    ratio = filters.CharFilter(field_name='ratio')
    output_type = filters.CharFilter(field_name='output_type')
    light_sens = filters.CharFilter(field_name='light_sens')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')
    formats = filters.ModelMultipleChoiceFilter(
        field_name='video_formats__format',
        to_field_name='format',
        queryset=VideoFormat.objects.all(),
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
                        "id": "tvl",
                        "type": "range",
                        "label": "TVL (Resolution)",
                        "field": "tvl",
                        "default_value": 1200
                    },
                    {
                        "id": "fov",
                        "type": "range",
                        "label": "Field of View",
                        "field": "fov",
                        "unit": "°",
                        "default_value": 140
                    },
                    {
                        "id": "voltage",
                        "type": "range",
                        "label": "Voltage Range",
                        "field": "voltage_min",
                        "unit": "V",
                        "default_value": 5
                    }
                ]
            },
            {
                "id": "output",
                "title": "Output & Format",
                "filters": [
                    {
                        "id": "output_type",
                        "type": "choice",
                        "label": "Output Type",
                        "field": "output_type"
                    },
                    {
                        "id": "ratio",
                        "type": "choice",
                        "label": "Aspect Ratio",
                        "field": "ratio"
                    },
                    {
                        "id": "formats",
                        "type": "choice",
                        "label": "Video Formats",
                        "field": "video_formats__format",
                        "model_field": "format"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "light_sens",
                        "type": "choice",
                        "label": "Light Sensitivity",
                        "field": "light_sens"
                    },
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
        model = Camera
        fields = [
            'manufacturer',
            'tvl_min', 'tvl_max',
            'voltage_min', 'voltage_max',
            'ratio', 'output_type',
            'fov_min', 'fov_max',
            'light_sens',
            'weight_min', 'weight_max',
            'formats'
        ]