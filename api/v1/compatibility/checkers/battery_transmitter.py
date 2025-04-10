from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class BatteryTransmitterCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between battery and transmitter.
    Checks if battery voltage is within transmitter's input voltage range.
    """

    def check_compatibility(self, battery, transmitter):

        issues = []

        # Check voltage compatibility
        if not hasattr(battery, 'voltage') or battery.voltage is None:
            issues.append({
                'type': 'missing_battery_info',
                'severity': 'critical',
                'message': 'Battery is missing voltage information',
                'component_refs': ['battery']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        if not hasattr(transmitter, 'input_voltage_min') or not hasattr(transmitter, 'input_voltage_max'):
            issues.append({
                'type': 'missing_transmitter_info',
                'severity': 'critical',
                'message': 'Transmitter is missing input voltage range information',
                'component_refs': ['transmitter']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Get battery voltage
        battery_voltage = battery.voltage

        # Get transmitter voltage range
        transmitter_min_voltage = transmitter.input_voltage_min
        transmitter_max_voltage = transmitter.input_voltage_max

        # Check if battery voltage is within transmitter's supported range
        if battery_voltage < transmitter_min_voltage or battery_voltage > transmitter_max_voltage:
            issues.append({
                'type': 'voltage_mismatch',
                'severity': 'critical',
                'message': f"Battery voltage ({battery_voltage}V) outside transmitter's supported input range ({transmitter_min_voltage}V-{transmitter_max_voltage}V)",
                'component_refs': ['battery', 'transmitter']
            })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'battery' or 'transmitter'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'battery' and hasattr(other_component, 'input_voltage_min') and hasattr(other_component,
                                                                                                     'input_voltage_max'):
            # Filtering batteries based on transmitter
            transmitter = other_component
            return {
                'min_voltage': transmitter.input_voltage_min,
                'max_voltage': transmitter.input_voltage_max
            }

        elif component_type == 'transmitter' and hasattr(other_component, 'voltage'):
            # Filtering transmitters based on battery
            battery = other_component
            return {
                'battery_voltage': battery.voltage
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'battery' or 'transmitter'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'battery':
            # Filtering batteries
            if 'min_voltage' in filter_params and 'max_voltage' in filter_params:
                min_voltage = filter_params['min_voltage']
                max_voltage = filter_params['max_voltage']
                queryset = queryset.filter(voltage__gte=min_voltage, voltage__lte=max_voltage)

        elif component_type == 'transmitter':
            # Filtering transmitters
            if 'battery_voltage' in filter_params:
                battery_voltage = filter_params['battery_voltage']
                queryset = queryset.filter(
                    input_voltage_min__lte=battery_voltage,
                    input_voltage_max__gte=battery_voltage
                )

        return queryset.distinct()


# Register this checker with the registry
register_checker('battery', 'transmitter', BatteryTransmitterCompatibilityChecker)