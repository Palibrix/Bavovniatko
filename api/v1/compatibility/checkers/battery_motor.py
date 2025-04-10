from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class BatteryMotorCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between battery and motor.
    Checks if battery cell count is within motor's supported range.
    """

    def check_compatibility(self, battery, motor):

        issues = []

        # Check cell count compatibility
        if not hasattr(battery, 'series') or battery.series is None:
            issues.append({
                'type': 'missing_battery_info',
                'severity': 'critical',
                'message': 'Battery is missing cell count information',
                'component_refs': ['battery']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Get motor details which contain voltage information
        if not motor.details.exists():
            issues.append({
                'type': 'missing_motor_details',
                'severity': 'critical',
                'message': 'Motor is missing voltage range information',
                'component_refs': ['motor']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Check each motor detail for voltage compatibility
        battery_series = battery.series
        battery_voltage = battery.voltage

        compatible_details = []
        for detail in motor.details.all():
            if hasattr(detail, 'voltage') and detail.voltage:
                if hasattr(detail.voltage, 'min_cells') and hasattr(detail.voltage, 'max_cells'):
                    min_cells = detail.voltage.min_cells
                    max_cells = detail.voltage.max_cells

                    if min_cells <= battery_series <= max_cells:
                        compatible_details.append(detail)

        if not compatible_details:
            # Format a message with all motor voltage ranges
            voltage_ranges = []
            for detail in motor.details.all():
                if hasattr(detail, 'voltage') and detail.voltage:
                    min_cells = getattr(detail.voltage, 'min_cells', None)
                    max_cells = getattr(detail.voltage, 'max_cells', None)
                    if min_cells is not None and max_cells is not None:
                        voltage_ranges.append(f"{min_cells}S-{max_cells}S")

            if voltage_ranges:
                voltage_range_str = ", ".join(voltage_ranges)
                message = f"Battery cell count ({battery_series}S) outside motor's supported ranges ({voltage_range_str})"
            else:
                message = f"Battery cell count ({battery_series}S) outside motor's supported range"

            issues.append({
                'type': 'cell_count_mismatch',
                'severity': 'critical',
                'message': message,
                'component_refs': ['battery', 'motor']
            })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'battery' or 'motor'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'battery' and hasattr(other_component, 'details'):
            # Filtering batteries based on motor
            motor = other_component
            if motor.details.exists():
                # Get all voltage ranges from motor details
                voltage_ranges = []
                for detail in motor.details.all():
                    if hasattr(detail, 'voltage') and detail.voltage:
                        min_cells = getattr(detail.voltage, 'min_cells', None)
                        max_cells = getattr(detail.voltage, 'max_cells', None)
                        if min_cells is not None and max_cells is not None:
                            voltage_ranges.append((min_cells, max_cells))

                if voltage_ranges:
                    return {'voltage_ranges': voltage_ranges}

        elif component_type == 'motor' and hasattr(other_component, 'series'):
            # Filtering motors based on battery
            battery = other_component
            return {
                'battery_series': battery.series
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'battery' or 'motor'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'battery':
            # Filtering batteries
            if 'voltage_ranges' in filter_params:
                voltage_ranges = filter_params['voltage_ranges']
                # Build a query for all voltage ranges
                q_obj = Q()
                for min_cells, max_cells in voltage_ranges:
                    q_obj |= Q(series__gte=min_cells, series__lte=max_cells)

                if q_obj:
                    queryset = queryset.filter(q_obj)

        elif component_type == 'motor':
            # Filtering motors
            if 'battery_series' in filter_params:
                battery_series = filter_params['battery_series']
                queryset = queryset.filter(
                    details__voltage__min_cells__lte=battery_series,
                    details__voltage__max_cells__gte=battery_series
                )

        return queryset.distinct()


# Register this checker with the registry
register_checker('battery', 'motor', BatteryMotorCompatibilityChecker)