from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class MotorSpeedControllerCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between motor and speed controller (ESC).
    Checks if ESC current rating is sufficient for motor's peak current.
    """

    def check_compatibility(self, motor, speed_controller):
        """
        Check if speed controller can handle motor's current requirements.

        Args:
            motor: Motor instance
            speed_controller: Speed Controller instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check current rating compatibility
        if not motor.details.exists():
            issues.append({
                'type': 'missing_motor_details',
                'severity': 'critical',
                'message': 'Motor is missing electrical specification details',
                'component_refs': ['motor']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        if not hasattr(speed_controller, 'cont_current') or not hasattr(speed_controller, 'burst_current'):
            issues.append({
                'type': 'missing_esc_current_ratings',
                'severity': 'critical',
                'message': 'Speed controller is missing current rating information',
                'component_refs': ['speed_controller']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Get motor peak current from its details
        motor_peak_current = None
        for detail in motor.details.all():
            if hasattr(detail, 'peak_current') and detail.peak_current is not None:
                motor_peak_current = detail.peak_current
                break

        if motor_peak_current is None:
            issues.append({
                'type': 'missing_motor_peak_current',
                'severity': 'critical',
                'message': 'Motor is missing peak current information',
                'component_refs': ['motor']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Get ESC current ratings
        esc_cont_current = speed_controller.cont_current
        esc_burst_current = speed_controller.burst_current

        # Check if ESC can handle motor's peak current
        if esc_cont_current < motor_peak_current:
            if esc_burst_current >= motor_peak_current:
                # Continuous current is too low, but burst current is sufficient
                issues.append({
                    'type': 'current_rating_warning',
                    'severity': 'warning',
                    'message': f"Motor peak current ({motor_peak_current}A) exceeds ESC continuous rating ({esc_cont_current}A), but within burst rating ({esc_burst_current}A)",
                    'component_refs': ['motor', 'speed_controller']
                })

                # Add running information
                issues.append({
                    'type': 'running_hot',
                    'severity': 'warning',
                    'message': f"ESC will likely run hot with this motor and might need additional cooling",
                    'component_refs': ['speed_controller']
                })
            else:
                # Both continuous and burst current ratings are insufficient
                issues.append({
                    'type': 'current_rating_insufficient',
                    'severity': 'critical',
                    'message': f"Speed controller current rating ({esc_cont_current}A continuous, {esc_burst_current}A burst) insufficient for motor peak current ({motor_peak_current}A)",
                    'component_refs': ['motor', 'speed_controller']
                })

        # Check for cell count compatibility if available
        if motor.details.exists() and hasattr(motor.details.first(), 'voltage') and \
                hasattr(speed_controller, 'voltage'):

            motor_voltage = motor.details.first().voltage
            esc_voltage = speed_controller.voltage

            if (hasattr(motor_voltage, 'min_cells') and hasattr(motor_voltage, 'max_cells') and
                    hasattr(esc_voltage, 'min_cells') and hasattr(esc_voltage, 'max_cells')):

                motor_min_cells = motor_voltage.min_cells
                motor_max_cells = motor_voltage.max_cells
                esc_min_cells = esc_voltage.min_cells
                esc_max_cells = esc_voltage.max_cells

                # Check for voltage range overlap
                if esc_max_cells < motor_min_cells or esc_min_cells > motor_max_cells:
                    issues.append({
                        'type': 'voltage_range_mismatch',
                        'severity': 'critical',
                        'message': f"Speed controller voltage range ({esc_min_cells}S-{esc_max_cells}S) doesn't overlap with motor range ({motor_min_cells}S-{motor_max_cells}S)",
                        'component_refs': ['motor', 'speed_controller']
                    })
                elif esc_max_cells < motor_max_cells:
                    issues.append({
                        'type': 'voltage_range_limitation',
                        'severity': 'warning',
                        'message': f"Speed controller limits maximum cell count to {esc_max_cells}S (motor supports up to {motor_max_cells}S)",
                        'component_refs': ['motor', 'speed_controller']
                    })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'motor' or 'speed_controller'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'motor' and hasattr(other_component, 'cont_current') and hasattr(other_component,
                                                                                              'burst_current'):
            # Filtering motors based on speed controller
            esc = other_component

            # Get ESC current ratings
            esc_current = esc.cont_current
            esc_burst = esc.burst_current

            # Get ESC voltage range if available
            esc_voltage_range = None
            if hasattr(esc, 'voltage') and hasattr(esc.voltage, 'min_cells') and hasattr(esc.voltage, 'max_cells'):
                esc_voltage_range = (esc.voltage.min_cells, esc.voltage.max_cells)

            return {
                'esc_current': esc_current,
                'esc_burst': esc_burst,
                'esc_voltage_range': esc_voltage_range
            }

        elif component_type == 'speed_controller' and hasattr(other_component, 'details'):
            # Filtering speed controllers based on motor
            motor = other_component

            if motor.details.exists():
                motor_detail = motor.details.first()

                # Get motor peak current if available
                motor_peak_current = getattr(motor_detail, 'peak_current', None)

                # Get motor voltage range if available
                motor_voltage_range = None
                if hasattr(motor_detail, 'voltage') and hasattr(motor_detail.voltage, 'min_cells') and hasattr(
                        motor_detail.voltage, 'max_cells'):
                    motor_voltage_range = (motor_detail.voltage.min_cells, motor_detail.voltage.max_cells)

                return {
                    'motor_peak_current': motor_peak_current,
                    'motor_voltage_range': motor_voltage_range
                }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'motor' or 'speed_controller'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'motor':
            # Filtering motors based on speed controller
            if 'esc_current' in filter_params and filter_params['esc_current'] is not None:
                esc_current = filter_params['esc_current']
                # Find motors with peak current <= ESC continuous current
                queryset = queryset.filter(details__peak_current__lte=esc_current)
            elif 'esc_burst' in filter_params and filter_params['esc_burst'] is not None:
                esc_burst = filter_params['esc_burst']
                # Find motors with peak current <= ESC burst current as a fallback
                queryset = queryset.filter(details__peak_current__lte=esc_burst)

            # Filter by voltage range if available
            if 'esc_voltage_range' in filter_params and filter_params['esc_voltage_range'] is not None:
                esc_min_cells, esc_max_cells = filter_params['esc_voltage_range']
                # Find motors with overlapping voltage ranges
                queryset = queryset.filter(
                    Q(details__voltage__min_cells__lte=esc_max_cells) &
                    Q(details__voltage__max_cells__gte=esc_min_cells)
                )

        elif component_type == 'speed_controller':
            # Filtering speed controllers based on motor
            if 'motor_peak_current' in filter_params and filter_params['motor_peak_current'] is not None:
                motor_peak_current = filter_params['motor_peak_current']
                # Find ESCs with continuous current or burst current >= motor peak current
                queryset = queryset.filter(
                    Q(cont_current__gte=motor_peak_current) |
                    Q(burst_current__gte=motor_peak_current)
                )

            # Filter by voltage range if available
            if 'motor_voltage_range' in filter_params and filter_params['motor_voltage_range'] is not None:
                motor_min_cells, motor_max_cells = filter_params['motor_voltage_range']
                # Find ESCs with overlapping voltage ranges
                queryset = queryset.filter(
                    Q(voltage__min_cells__lte=motor_max_cells) &
                    Q(voltage__max_cells__gte=motor_min_cells)
                )

        return queryset.distinct()


# Register this checker with the registry
register_checker('motor', 'speed_controller', MotorSpeedControllerCompatibilityChecker)