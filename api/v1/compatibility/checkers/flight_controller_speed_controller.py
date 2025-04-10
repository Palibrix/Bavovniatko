"""
Flight Controller-Speed Controller compatibility checker.
"""

from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class FlightControllerSpeedControllerCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between flight controller and speed controller (ESC).
    Checks if there are compatible communication protocols between FC and ESC.
    """

    def check_compatibility(self, flight_controller, speed_controller):
        """
        Check if flight controller and speed controller have compatible protocols.

        Args:
            flight_controller: Flight Controller instance
            speed_controller: Speed Controller instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check protocol compatibility
        if not hasattr(flight_controller, 'firmwares') or not flight_controller.firmwares.exists():
            issues.append({
                'type': 'missing_fc_firmware',
                'severity': 'warning',
                'message': 'Flight controller is missing firmware information',
                'component_refs': ['flight_controller']
            })

        if not hasattr(speed_controller, 'protocols') or not speed_controller.protocols.exists():
            issues.append({
                'type': 'missing_esc_protocols',
                'severity': 'critical',
                'message': 'Speed controller is missing protocol information',
                'component_refs': ['speed_controller']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Check for physical dimensions compatibility
        if hasattr(flight_controller, 'mount_length') and hasattr(flight_controller, 'mount_width') and \
                hasattr(speed_controller, 'mount_length') and hasattr(speed_controller, 'mount_width'):

            fc_length = flight_controller.mount_length
            fc_width = flight_controller.mount_width
            esc_length = speed_controller.mount_length
            esc_width = speed_controller.mount_width

            # Check if dimensions match (allowing for both orientations)
            if not ((fc_length == esc_length and fc_width == esc_width) or
                    (fc_length == esc_width and fc_width == esc_length)):
                issues.append({
                    'type': 'dimension_mismatch',
                    'severity': 'critical',
                    'message': f"Flight controller dimensions ({fc_length}x{fc_width}mm) don't match speed controller dimensions ({esc_length}x{esc_width}mm)",
                    'component_refs': ['flight_controller', 'speed_controller']
                })

        # For protocol compatibility, we'll simply check that the speed controller has protocols
        # and assume firmware-protocol compatibility is maintained in the database

        esc_protocol_types = [p.protocol for p in speed_controller.protocols.all()]
        fc_firmware_types = []
        if hasattr(flight_controller, 'firmwares') and flight_controller.firmwares.exists():
            fc_firmware_types = [fw.firmware for fw in flight_controller.firmwares.all()]

        # Add informational message about protocols and firmwares
        if fc_firmware_types:
            issues.append({
                'type': 'protocol_info',
                'severity': 'info',
                'message': f"FC firmwares: {', '.join(fc_firmware_types)}, ESC protocols: {', '.join(esc_protocol_types)}",
                'component_refs': ['flight_controller', 'speed_controller']
            })
        else:
            issues.append({
                'type': 'protocol_info',
                'severity': 'info',
                'message': f"ESC protocols: {', '.join(esc_protocol_types)}",
                'component_refs': ['speed_controller']
            })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'flight_controller' or 'speed_controller'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'flight_controller' and hasattr(other_component, 'mount_length') and hasattr(
                other_component, 'mount_width'):
            # Filtering flight controllers based on speed controller
            esc = other_component
            return {
                'esc_dimensions': (esc.mount_length, esc.mount_width)
            }

        elif component_type == 'speed_controller' and hasattr(other_component, 'mount_length') and hasattr(
                other_component, 'mount_width'):
            # Filtering speed controllers based on flight controller
            fc = other_component
            return {
                'fc_dimensions': (fc.mount_length, fc.mount_width)
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'flight_controller' or 'speed_controller'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        # Filter only by mounting dimensions if provided
        if component_type == 'flight_controller' and 'esc_dimensions' in filter_params and filter_params[
            'esc_dimensions']:
            esc_length, esc_width = filter_params['esc_dimensions']
            queryset = queryset.filter(
                Q(mount_length=esc_length, mount_width=esc_width) |
                Q(mount_length=esc_width, mount_width=esc_length)
            )

        elif component_type == 'speed_controller' and 'fc_dimensions' in filter_params and filter_params[
            'fc_dimensions']:
            fc_length, fc_width = filter_params['fc_dimensions']
            queryset = queryset.filter(
                Q(mount_length=fc_length, mount_width=fc_width) |
                Q(mount_length=fc_width, mount_width=fc_length)
            )

        return queryset.distinct()


# Register this checker with the registry
register_checker('flight_controller', 'speed_controller', FlightControllerSpeedControllerCompatibilityChecker)