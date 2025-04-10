"""
Receiver-Flight Controller compatibility checker.
"""

from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class ReceiverFlightControllerCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between receiver and flight controller.
    Checks if there are compatible communication protocols between receiver and FC.
    """

    def check_compatibility(self, flight_controller, receiver):
        """
        Check if receiver and flight controller have compatible protocols.

        Args:
            flight_controller: Flight Controller instance
            receiver: Receiver instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check protocol compatibility
        if not hasattr(receiver, 'protocols') or not receiver.protocols.exists():
            issues.append({
                'type': 'missing_receiver_protocols',
                'severity': 'critical',
                'message': 'Receiver is missing protocol information',
                'component_refs': ['receiver']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        if not hasattr(flight_controller, 'firmwares') or not flight_controller.firmwares.exists():
            issues.append({
                'type': 'missing_fc_firmware',
                'severity': 'warning',
                'message': 'Flight controller is missing firmware information',
                'component_refs': ['flight_controller']
            })
            # Not critical, because most modern FCs support all common receiver protocols

        # Get receiver protocols and FC firmware info
        receiver_protocols = [protocol.type for protocol in receiver.protocols.all()]

        fc_firmware_types = []
        if hasattr(flight_controller, 'firmwares'):
            fc_firmware_types = [fw.firmware for fw in flight_controller.firmwares.all()]

        # Add informational message about protocols
        if fc_firmware_types:
            issues.append({
                'type': 'protocol_info',
                'severity': 'info',
                'message': f"FC firmwares: {', '.join(fc_firmware_types)}, Receiver protocols: {', '.join(receiver_protocols)}",
                'component_refs': ['flight_controller', 'receiver']
            })
        else:
            issues.append({
                'type': 'protocol_info',
                'severity': 'info',
                'message': f"Receiver protocols: {', '.join(receiver_protocols)}",
                'component_refs': ['receiver']
            })

        # Check physical connectivity if both have processor/MCU information
        if hasattr(receiver, 'processor') and receiver.processor and \
                hasattr(flight_controller, 'microcontroller') and flight_controller.microcontroller:
            # This is purely informational
            issues.append({
                'type': 'processor_info',
                'severity': 'info',
                'message': f"Receiver processor: {receiver.processor}, FC processor: {flight_controller.microcontroller}",
                'component_refs': ['receiver', 'flight_controller']
            })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'receiver' or 'flight_controller'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        # No specific filtering needed for this relationship
        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'receiver' or 'flight_controller'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        # No specific filtering for this relationship
        return queryset.distinct()


# Register this checker with the registry
register_checker('flight_controller', 'receiver', ReceiverFlightControllerCompatibilityChecker)