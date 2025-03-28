from django_filters import rest_framework as filters

from api.mixins import MetadataFilterSet
from components.models import FlightController, Stack, SpeedController, SpeedControllerProtocol, \
    SpeedControllerFirmware, FlightControllerFirmware


class StackFilter(MetadataFilterSet):
    """
    Filter for Stacks with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    gyro_max_freq_min = filters.NumberFilter(field_name='flight_controller__gyro__max_freq', lookup_expr='gte')
    gyro_max_freq_max = filters.NumberFilter(field_name='flight_controller__gyro__max_freq', lookup_expr='lte')

    cont_current_min = filters.NumberFilter(field_name='speed_controller__cont_current', lookup_expr='gte')
    cont_current_max = filters.NumberFilter(field_name='speed_controller__cont_current', lookup_expr='lte')

    burst_current_min = filters.NumberFilter(field_name='speed_controller__burst_current', lookup_expr='gte')
    burst_current_max = filters.NumberFilter(field_name='speed_controller__burst_current', lookup_expr='lte')

    fc_mount_length_min = filters.NumberFilter(field_name='flight_controller__mount_length', lookup_expr='gte')
    fc_mount_length_max = filters.NumberFilter(field_name='flight_controller__mount_length', lookup_expr='lte')

    fc_mount_width_min = filters.NumberFilter(field_name='flight_controller__mount_width', lookup_expr='gte')
    fc_mount_width_max = filters.NumberFilter(field_name='flight_controller__mount_width', lookup_expr='lte')

    sc_mount_length_min = filters.NumberFilter(field_name='speed_controller__mount_length', lookup_expr='gte')
    sc_mount_length_max = filters.NumberFilter(field_name='speed_controller__mount_length', lookup_expr='lte')

    sc_mount_width_min = filters.NumberFilter(field_name='speed_controller__mount_width', lookup_expr='gte')
    sc_mount_width_max = filters.NumberFilter(field_name='speed_controller__mount_width', lookup_expr='lte')

    # Choice filters
    fc_bluetooth = filters.BooleanFilter(field_name='flight_controller__bluetooth')
    fc_wifi = filters.BooleanFilter(field_name='flight_controller__wifi')
    fc_barometer = filters.BooleanFilter(field_name='flight_controller__barometer')
    fc_gyro_imu = filters.CharFilter(field_name='flight_controller__gyro__imu')
    fc_gyro_spi = filters.BooleanFilter(field_name='flight_controller__gyro__spi_support')
    fc_connector_type = filters.CharFilter(field_name='flight_controller__connector_type')

    sc_is_wireless = filters.BooleanFilter(field_name='speed_controller__is_wireless_conf')
    sc_esc_type = filters.CharFilter(field_name='speed_controller__esc_type')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')
    fc_manufacturer = filters.BaseInFilter(field_name='flight_controller__manufacturer')
    sc_manufacturer = filters.BaseInFilter(field_name='speed_controller__manufacturer')

    flight_controller = filters.ModelChoiceFilter(queryset=FlightController.objects.all())
    speed_controller = filters.ModelChoiceFilter(queryset=SpeedController.objects.all())

    fc_min_cells = filters.BaseInFilter(field_name='flight_controller__voltage__min_cells')
    fc_max_cells = filters.BaseInFilter(field_name='flight_controller__voltage__max_cells')

    sc_min_cells = filters.BaseInFilter(field_name='speed_controller__voltage__min_cells')
    sc_max_cells = filters.BaseInFilter(field_name='speed_controller__voltage__max_cells')

    flight_controller_firmwares = filters.ModelMultipleChoiceFilter(
        field_name='flight_controller__firmwares__firmware',
        to_field_name='firmware',
        queryset=FlightControllerFirmware.objects.all(),
        conjoined=True,
    )

    speed_controller_protocols = filters.ModelMultipleChoiceFilter(
        field_name='speed_controller__protocols__protocol',
        to_field_name='protocol',
        queryset=SpeedControllerProtocol.objects.all(),
        conjoined=True,
    )

    speed_controller_firmwares = filters.ModelMultipleChoiceFilter(
        field_name='speed_controller__firmwares__firmware',
        to_field_name='firmware',
        queryset=SpeedControllerFirmware.objects.all(),
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
                        "label": "Stack Manufacturer",
                        "field": "manufacturer",
                        "searchable": True,
                    },
                    {
                        "id": "fc_manufacturer",
                        "type": "choice",
                        "label": "FC Manufacturer",
                        "field": "flight_controller__manufacturer",
                        "searchable": True,
                    },
                    {
                        "id": "sc_manufacturer",
                        "type": "choice",
                        "label": "ESC Manufacturer",
                        "field": "speed_controller__manufacturer",
                        "searchable": True,
                    }
                ]
            },
            {
                "id": "components",
                "title": "Stack Components",
                "filters": [
                    {
                        "id": "flight_controller",
                        "type": "model",
                        "label": "Flight Controller",
                        "field": "flight_controller"
                    },
                    {
                        "id": "speed_controller",
                        "type": "model",
                        "label": "Speed Controller",
                        "field": "speed_controller"
                    }
                ]
            },
            {
                "id": "flight_controller",
                "title": "Flight Controller Features",
                "filters": [
                    {
                        "id": "fc_gyro_imu",
                        "type": "choice",
                        "label": "Gyro IMU",
                        "field": "flight_controller__gyro__imu"
                    },
                    {
                        "id": "gyro_max_freq",
                        "type": "range",
                        "label": "Gyro Max Frequency",
                        "field": "flight_controller__gyro__max_freq",
                        "unit": "kHz",
                        "default_value": 8
                    },
                    {
                        "id": "fc_gyro_spi",
                        "type": "boolean",
                        "label": "SPI Support",
                        "field": "flight_controller__gyro__spi_support"
                    },
                    {
                        "id": "fc_bluetooth",
                        "type": "boolean",
                        "label": "Has Bluetooth",
                        "field": "flight_controller__bluetooth"
                    },
                    {
                        "id": "fc_wifi",
                        "type": "boolean",
                        "label": "Has WiFi",
                        "field": "flight_controller__wifi"
                    },
                    {
                        "id": "fc_barometer",
                        "type": "boolean",
                        "label": "Has Barometer",
                        "field": "flight_controller__barometer"
                    },
                    {
                        "id": "fc_connector_type",
                        "type": "choice",
                        "label": "Connector Type",
                        "field": "flight_controller__connector_type"
                    },
                    {
                        "id": "fc_min_cells",
                        "type": "choice",
                        "label": "Min Cells",
                        "field": "flight_controller__voltage__min_cells"
                    },
                    {
                        "id": "fc_max_cells",
                        "type": "choice",
                        "label": "Max Cells",
                        "field": "flight_controller__voltage__max_cells"
                    },
                    {
                        "id": "flight_controller_firmwares",
                        "type": "choice",
                        "label": "Firmware",
                        "field": "flight_controller__firmwares__firmware",
                        "model_field": "firmware"
                    }
                ]
            },
            {
                "id": "speed_controller",
                "title": "Speed Controller Features",
                "filters": [
                    {
                        "id": "sc_is_wireless",
                        "type": "boolean",
                        "label": "Wireless Configuration",
                        "field": "speed_controller__is_wireless_conf"
                    },
                    {
                        "id": "sc_esc_type",
                        "type": "choice",
                        "label": "ESC Type",
                        "field": "speed_controller__esc_type"
                    },
                    {
                        "id": "cont_current",
                        "type": "range",
                        "label": "Continuous Current",
                        "field": "speed_controller__cont_current",
                        "unit": "A",
                        "default_value": 30
                    },
                    {
                        "id": "burst_current",
                        "type": "range",
                        "label": "Burst Current",
                        "field": "speed_controller__burst_current",
                        "unit": "A",
                        "default_value": 40
                    },
                    {
                        "id": "sc_min_cells",
                        "type": "choice",
                        "label": "Min Cells",
                        "field": "speed_controller__voltage__min_cells"
                    },
                    {
                        "id": "sc_max_cells",
                        "type": "choice",
                        "label": "Max Cells",
                        "field": "speed_controller__voltage__max_cells"
                    },
                    {
                        "id": "speed_controller_protocols",
                        "type": "choice",
                        "label": "Protocols",
                        "field": "speed_controller__protocols__protocol",
                        "model_field": "protocol"
                    },
                    {
                        "id": "speed_controller_firmwares",
                        "type": "choice",
                        "label": "Firmware",
                        "field": "speed_controller__firmwares__firmware",
                        "model_field": "firmware"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "fc_mount",
                        "type": "range",
                        "label": "FC Mount Length",
                        "field": "flight_controller__mount_length",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "fc_mount_width",
                        "type": "range",
                        "label": "FC Mount Width",
                        "field": "flight_controller__mount_width",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "sc_mount_length",
                        "type": "range",
                        "label": "ESC Mount Length",
                        "field": "speed_controller__mount_length",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "sc_mount_width",
                        "type": "range",
                        "label": "ESC Mount Width",
                        "field": "speed_controller__mount_width",
                        "unit": "mm",
                        "default_value": 30.5
                    }
                ]
            }
        ]
    }

    class Meta:
        model = Stack
        fields = [
            'manufacturer', 'fc_manufacturer', 'sc_manufacturer',
            'flight_controller', 'speed_controller',
            'fc_gyro_imu', 'fc_gyro_spi',
            'gyro_max_freq_min', 'gyro_max_freq_max',
            'fc_bluetooth', 'fc_wifi', 'fc_barometer',
            'fc_connector_type',
            'fc_min_cells', 'fc_max_cells',
            'fc_mount_length_min', 'fc_mount_length_max',
            'fc_mount_width_min', 'fc_mount_width_max',
            'flight_controller_firmwares',
            'sc_is_wireless', 'sc_esc_type',
            'cont_current_min', 'cont_current_max',
            'burst_current_min', 'burst_current_max',
            'sc_min_cells', 'sc_max_cells',
            'sc_mount_length_min', 'sc_mount_length_max',
            'sc_mount_width_min', 'sc_mount_width_max',
            'speed_controller_protocols',
            'speed_controller_firmwares'
        ]


class FlightControllerFilter(MetadataFilterSet):
    """
    Filter for Flight Controllers with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    gyro_max_freq_min = filters.NumberFilter(field_name='gyro__max_freq', lookup_expr='gte')
    gyro_max_freq_max = filters.NumberFilter(field_name='gyro__max_freq', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    mount_length_min = filters.NumberFilter(field_name='mount_length', lookup_expr='gte')
    mount_length_max = filters.NumberFilter(field_name='mount_length', lookup_expr='lte')

    mount_width_min = filters.NumberFilter(field_name='mount_width', lookup_expr='gte')
    mount_width_max = filters.NumberFilter(field_name='mount_width', lookup_expr='lte')

    # Choice and boolean filters
    in_stack = filters.BooleanFilter(field_name='stack', lookup_expr='isnull', exclude=True)
    bluetooth = filters.BooleanFilter(field_name='bluetooth')
    wifi = filters.BooleanFilter(field_name='wifi')
    barometer = filters.BooleanFilter(field_name='barometer')
    connector_type = filters.CharFilter(field_name='connector_type')
    gyro_imu = filters.CharFilter(field_name='gyro__imu')
    gyro_spi_support = filters.BooleanFilter(field_name='gyro__spi_support')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')
    min_cells = filters.BaseInFilter(field_name='voltage__min_cells')
    max_cells = filters.BaseInFilter(field_name='voltage__max_cells')

    firmwares = filters.ModelMultipleChoiceFilter(
        field_name='firmwares__firmware',
        to_field_name='firmware',
        queryset=FlightControllerFirmware.objects.all(),
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
                "id": "features",
                "title": "Features",
                "filters": [
                    {
                        "id": "bluetooth",
                        "type": "boolean",
                        "label": "Has Bluetooth",
                        "field": "bluetooth"
                    },
                    {
                        "id": "wifi",
                        "type": "boolean",
                        "label": "Has WiFi",
                        "field": "wifi"
                    },
                    {
                        "id": "barometer",
                        "type": "boolean",
                        "label": "Has Barometer",
                        "field": "barometer"
                    },
                    {
                        "id": "connector_type",
                        "type": "choice",
                        "label": "Connector Type",
                        "field": "connector_type"
                    },
                    {
                        "id": "in_stack",
                        "type": "boolean",
                        "label": "Part of Stack",
                        "field": "in_stack"
                    }
                ]
            },
            {
                "id": "gyro",
                "title": "Gyro Specifications",
                "filters": [
                    {
                        "id": "gyro_imu",
                        "type": "choice",
                        "label": "Gyro IMU",
                        "field": "gyro__imu"
                    },
                    {
                        "id": "gyro_max_freq",
                        "type": "range",
                        "label": "Gyro Max Frequency",
                        "field": "gyro__max_freq",
                        "unit": "kHz",
                        "default_value": 8
                    },
                    {
                        "id": "gyro_spi_support",
                        "type": "boolean",
                        "label": "SPI Support",
                        "field": "gyro__spi_support"
                    }
                ]
            },
            {
                "id": "power",
                "title": "Power Requirements",
                "filters": [
                    {
                        "id": "min_cells",
                        "type": "choice",
                        "label": "Min Cells",
                        "field": "voltage__min_cells"
                    },
                    {
                        "id": "max_cells",
                        "type": "choice",
                        "label": "Max Cells",
                        "field": "voltage__max_cells"
                    }
                ]
            },
            {
                "id": "firmware",
                "title": "Firmware",
                "filters": [
                    {
                        "id": "firmwares",
                        "type": "choice",
                        "label": "Supported Firmware",
                        "field": "firmwares__firmware",
                        "model_field": "firmware"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "mount_length",
                        "type": "range",
                        "label": "Mount Length",
                        "field": "mount_length",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "mount_width",
                        "type": "range",
                        "label": "Mount Width",
                        "field": "mount_width",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "weight",
                        "type": "range",
                        "label": "Weight",
                        "field": "weight",
                        "unit": "g",
                        "default_value": 10
                    }
                ]
            }
        ]
    }

    class Meta:
        model = FlightController
        fields = [
            'manufacturer',
            'bluetooth', 'wifi', 'barometer',
            'connector_type',
            'gyro_imu', 'gyro_spi_support',
            'gyro_max_freq_min', 'gyro_max_freq_max',
            'mount_length_min', 'mount_length_max',
            'mount_width_min', 'mount_width_max',
            'min_cells', 'max_cells',
            'firmwares',
            'in_stack',
            'weight_min', 'weight_max'
        ]


class SpeedControllerFilter(MetadataFilterSet):
    """
    Filter for Speed Controllers with UI metadata support.
    Defines both the filter logic and the UI structure.
    """
    # Range filters
    cont_current_min = filters.NumberFilter(field_name='cont_current', lookup_expr='gte')
    cont_current_max = filters.NumberFilter(field_name='cont_current', lookup_expr='lte')

    burst_current_min = filters.NumberFilter(field_name='burst_current', lookup_expr='gte')
    burst_current_max = filters.NumberFilter(field_name='burst_current', lookup_expr='lte')

    weight_min = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    mount_length_min = filters.NumberFilter(field_name='mount_length', lookup_expr='gte')
    mount_length_max = filters.NumberFilter(field_name='mount_length', lookup_expr='lte')

    mount_width_min = filters.NumberFilter(field_name='mount_width', lookup_expr='gte')
    mount_width_max = filters.NumberFilter(field_name='mount_width', lookup_expr='lte')

    # Choice and boolean filters
    in_stack = filters.BooleanFilter(field_name='stack', lookup_expr='isnull', exclude=True)
    is_wireless_conf = filters.BooleanFilter(field_name='is_wireless_conf')
    esc_type = filters.CharFilter(field_name='esc_type')

    # Multi-select filters
    manufacturer = filters.BaseInFilter(field_name='manufacturer')
    min_cells = filters.BaseInFilter(field_name='voltage__min_cells')
    max_cells = filters.BaseInFilter(field_name='voltage__max_cells')

    protocols = filters.ModelMultipleChoiceFilter(
        field_name='protocols__protocol',
        to_field_name='protocol',
        queryset=SpeedControllerProtocol.objects.all(),
        conjoined=True,
    )

    firmwares = filters.ModelMultipleChoiceFilter(
        field_name='firmwares__firmware',
        to_field_name='firmware',
        queryset=SpeedControllerFirmware.objects.all(),
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
                "id": "features",
                "title": "Features",
                "filters": [
                    {
                        "id": "is_wireless_conf",
                        "type": "boolean",
                        "label": "Wireless Configuration",
                        "field": "is_wireless_conf"
                    },
                    {
                        "id": "esc_type",
                        "type": "choice",
                        "label": "ESC Type",
                        "field": "esc_type"
                    },
                    {
                        "id": "in_stack",
                        "type": "boolean",
                        "label": "Part of Stack",
                        "field": "in_stack"
                    }
                ]
            },
            {
                "id": "performance",
                "title": "Performance",
                "filters": [
                    {
                        "id": "cont_current",
                        "type": "range",
                        "label": "Continuous Current",
                        "field": "cont_current",
                        "unit": "A",
                        "default_value": 30
                    },
                    {
                        "id": "burst_current",
                        "type": "range",
                        "label": "Burst Current",
                        "field": "burst_current",
                        "unit": "A",
                        "default_value": 40
                    }
                ]
            },
            {
                "id": "power",
                "title": "Power Requirements",
                "filters": [
                    {
                        "id": "min_cells",
                        "type": "choice",
                        "label": "Min Cells",
                        "field": "voltage__min_cells"
                    },
                    {
                        "id": "max_cells",
                        "type": "choice",
                        "label": "Max Cells",
                        "field": "voltage__max_cells"
                    }
                ]
            },
            {
                "id": "protocols",
                "title": "Protocols & Firmware",
                "filters": [
                    {
                        "id": "protocols",
                        "type": "choice",
                        "label": "Supported Protocols",
                        "field": "protocols__protocol",
                        "model_field": "protocol"
                    },
                    {
                        "id": "firmwares",
                        "type": "choice",
                        "label": "Supported Firmware",
                        "field": "firmwares__firmware",
                        "model_field": "firmware"
                    }
                ]
            },
            {
                "id": "physical",
                "title": "Physical Characteristics",
                "filters": [
                    {
                        "id": "mount_length",
                        "type": "range",
                        "label": "Mount Length",
                        "field": "mount_length",
                        "unit": "mm",
                        "default_value": 30.5
                    },
                    {
                        "id": "mount_width",
                        "type": "range",
                        "label": "Mount Width",
                        "field": "mount_width",
                        "unit": "mm",
                        "default_value": 30.5
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
        model = SpeedController
        fields = [
            'manufacturer',
            'is_wireless_conf', 'esc_type',
            'cont_current_min', 'cont_current_max',
            'burst_current_min', 'burst_current_max',
            'mount_length_min', 'mount_length_max',
            'mount_width_min', 'mount_width_max',
            'min_cells', 'max_cells',
            'protocols', 'firmwares',
            'in_stack',
            'weight_min', 'weight_max'
        ]