from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import Frame


class FrameFilter(MetadataFilterSet):
    """
    Filter for Frames with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    camera_mount_height_min = filters.NumberFilter(field_name='camera_details__camera_mount_height', lookup_expr='gte')
    camera_mount_height_max = filters.NumberFilter(field_name='camera_details__camera_mount_height', lookup_expr='lte')

    camera_mount_width_min = filters.NumberFilter(field_name='camera_details__camera_mount_width', lookup_expr='gte')
    camera_mount_width_max = filters.NumberFilter(field_name='camera_details__camera_mount_width', lookup_expr='lte')

    motor_mount_height_min = filters.NumberFilter(field_name='motor_details__motor_mount_height', lookup_expr='gte')
    motor_mount_height_max = filters.NumberFilter(field_name='motor_details__motor_mount_height', lookup_expr='lte')

    motor_mount_width_min = filters.NumberFilter(field_name='motor_details__motor_mount_width', lookup_expr='gte')
    motor_mount_width_max = filters.NumberFilter(field_name='motor_details__motor_mount_width', lookup_expr='lte')

    vtx_mount_height_min = filters.NumberFilter(field_name='vtx_details__vtx_mount_height', lookup_expr='gte')
    vtx_mount_height_max = filters.NumberFilter(field_name='vtx_details__vtx_mount_height', lookup_expr='lte')

    vtx_mount_width_min = filters.NumberFilter(field_name='vtx_details__vtx_mount_width', lookup_expr='gte')
    vtx_mount_width_max = filters.NumberFilter(field_name='vtx_details__vtx_mount_width', lookup_expr='lte')

    # Choice filters
    prop_size = filters.CharFilter(field_name='prop_size')
    size = filters.CharFilter(field_name='size')
    material = filters.CharFilter(field_name='material')
    configuration = filters.CharFilter(field_name='configuration')

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
                "title": "Frame Dimensions",
                "filters": [
                    {
                        "id": "size",
                        "type": "choice",
                        "label": "Frame Size",
                        "field": "size"
                    },
                    {
                        "id": "prop_size",
                        "type": "choice",
                        "label": "Propeller Size",
                        "field": "prop_size"
                    },
                    {
                        "id": "weight",
                        "type": "range",
                        "label": "Weight",
                        "field": "weight",
                        "unit": "g",
                        "default_value": 120
                    }
                ]
            },
            {
                "id": "properties",
                "title": "Frame Properties",
                "filters": [
                    {
                        "id": "material",
                        "type": "choice",
                        "label": "Material",
                        "field": "material"
                    },
                    {
                        "id": "configuration",
                        "type": "choice",
                        "label": "Configuration",
                        "field": "configuration"
                    }
                ]
            },
            {
                "id": "camera_mount",
                "title": "Camera Mount",
                "filters": [
                    {
                        "id": "camera_mount_height",
                        "type": "range",
                        "label": "Camera Mount Height",
                        "field": "camera_details__camera_mount_height",
                        "unit": "mm",
                        "default_value": 19
                    },
                    {
                        "id": "camera_mount_width",
                        "type": "range",
                        "label": "Camera Mount Width",
                        "field": "camera_details__camera_mount_width",
                        "unit": "mm",
                        "default_value": 19
                    }
                ]
            },
            {
                "id": "motor_mount",
                "title": "Motor Mount",
                "filters": [
                    {
                        "id": "motor_mount_height",
                        "type": "range",
                        "label": "Motor Mount Height",
                        "field": "motor_details__motor_mount_height",
                        "unit": "mm",
                        "default_value": 16
                    },
                    {
                        "id": "motor_mount_width",
                        "type": "range",
                        "label": "Motor Mount Width",
                        "field": "motor_details__motor_mount_width",
                        "unit": "mm",
                        "default_value": 16
                    }
                ]
            },
            {
                "id": "vtx_mount",
                "title": "VTX Mount",
                "filters": [
                    {
                        "id": "vtx_mount_height",
                        "type": "range",
                        "label": "VTX Mount Height",
                        "field": "vtx_details__vtx_mount_height",
                        "unit": "mm",
                        "default_value": 20
                    },
                    {
                        "id": "vtx_mount_width",
                        "type": "range",
                        "label": "VTX Mount Width",
                        "field": "vtx_details__vtx_mount_width",
                        "unit": "mm",
                        "default_value": 20
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Frame
        fields = [
            'manufacturer',
            'prop_size', 'size',
            'weight_min', 'weight_max',
            'material', 'configuration',
            'camera_mount_height_min', 'camera_mount_height_max',
            'camera_mount_width_min', 'camera_mount_width_max',
            'motor_mount_height_min', 'motor_mount_height_max',
            'motor_mount_width_min', 'motor_mount_width_max',
            'vtx_mount_height_min', 'vtx_mount_height_max',
            'vtx_mount_width_min', 'vtx_mount_width_max'
        ]