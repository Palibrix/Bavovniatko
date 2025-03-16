from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Antenna, AntennaConnector


class AntennaFilter(MetadataFilterSet):
    """
    Filter for Antennas with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    center_frequency = filters.RangeFilter(field_name='center_frequency')
    swr = filters.RangeFilter(field_name='swr',)
    gain = filters.RangeFilter(field_name='gain')
    radiation = filters.RangeFilter(field_name='radiation')
    weight = filters.RangeFilter(field_name='details__weight')

    # Define UI metadata for the filters - structure matches the HTML prototype
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
                        "searchable": True
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
                        "default_value": 3000  # Default value for the slider
                    },
                    {
                        "id": "swr",
                        "type": "range",
                        "label": "SWR (VSWR)",
                        "field": "swr",
                        "default_value": 2  # Default value for the slider
                    },
                    {
                        "id": "gain",
                        "type": "range",
                        "label": "Gain",
                        "field": "gain",
                        "unit": "dBi",
                        "default_value": 7.5  # Default value for the slider
                    },
                    {
                        "id": "radiation",
                        "type": "range",
                        "label": "Radiation Efficiency",
                        "field": "radiation",
                        "unit": "%",
                        "default_value": 50  # Default value for the slider
                    }
                ]
            },
            {
                "id": "antenna_type",
                "title": "Antenna Type",
                "filters": [
                    {
                        "id": "type",
                        "type": "choice",
                        "label": "Type",
                        "field": "type__type"
                    },
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
                        "model_field": "type"  # Use this field for display value
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
                        "default_value": 15  # Default value for the slider
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Antenna
        fields = ['manufacturer', 'center_frequency', 'bandwidth_min', 'bandwidth_max',
                  'swr', 'gain', 'radiation',
                  'type__type', 'type__direction', 'type__polarization',
                  'details__connector_type__type', 'details__angle_type',
                  'weight']