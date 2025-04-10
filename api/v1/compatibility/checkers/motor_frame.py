from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class MotorFrameCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between motor and frame.
    Checks if motor mount dimensions match frame motor mount dimensions.
    """

    def check_compatibility(self, frame, motor):
        """
        Check if motor is compatible with frame.

        Args:
            motor: Motor instance
            frame: Frame instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check motor mount compatibility
        if not hasattr(motor, 'mount_height') or not hasattr(motor, 'mount_width'):
            issues.append({
                'type': 'missing_motor_dimensions',
                'severity': 'critical',
                'message': 'Motor is missing mounting dimension information',
                'component_refs': ['motor']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        if not frame.motor_details.exists():
            issues.append({
                'type': 'missing_frame_motor_mounts',
                'severity': 'critical',
                'message': 'Frame is missing motor mount information',
                'component_refs': ['frame']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Check if any frame motor mount matches the motor dimensions
        motor_height = motor.mount_height
        motor_width = motor.mount_width

        motor_mount_match = False
        matching_mount = None

        for frame_motor_detail in frame.motor_details.all():
            if (frame_motor_detail.motor_mount_height == motor_height and
                    frame_motor_detail.motor_mount_width == motor_width):
                motor_mount_match = True
                matching_mount = frame_motor_detail
                break

        if not motor_mount_match:
            # Format error message with available motor mounts
            mount_options = [
                f"{detail.motor_mount_height}x{detail.motor_mount_width}mm"
                for detail in frame.motor_details.all()
            ]
            mount_options_str = ", ".join(mount_options)

            issues.append({
                'type': 'motor_mount_mismatch',
                'severity': 'critical',
                'message': f"Motor mount dimensions ({motor_height}x{motor_width}mm) don't match any frame motor mounts ({mount_options_str})",
                'component_refs': ['motor', 'frame']
            })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'motor' or 'frame'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'motor' and hasattr(other_component, 'motor_details'):
            # Filtering motors based on frame
            frame = other_component
            if frame.motor_details.exists():
                # Get all frame motor mount dimensions
                mount_dimensions = [
                    (detail.motor_mount_height, detail.motor_mount_width)
                    for detail in frame.motor_details.all()
                ]

                return {'mount_dimensions': mount_dimensions}

        elif component_type == 'frame' and hasattr(other_component, 'mount_height') and hasattr(other_component,
                                                                                                'mount_width'):
            # Filtering frames based on motor
            motor = other_component
            return {
                'motor_height': motor.mount_height,
                'motor_width': motor.mount_width
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'motor' or 'frame'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'motor':
            # Filtering motors
            if 'mount_dimensions' in filter_params and filter_params['mount_dimensions']:
                mount_dimensions = filter_params['mount_dimensions']

                # Build a query for all mount dimensions
                q_obj = Q()
                for height, width in mount_dimensions:
                    q_obj |= Q(mount_height=height, mount_width=width)

                if q_obj:
                    queryset = queryset.filter(q_obj)

        elif component_type == 'frame':
            # Filtering frames
            if 'motor_height' in filter_params and 'motor_width' in filter_params:
                motor_height = filter_params['motor_height']
                motor_width = filter_params['motor_width']

                queryset = queryset.filter(
                    motor_details__motor_mount_height=motor_height,
                    motor_details__motor_mount_width=motor_width
                )

        return queryset.distinct()


# Register this checker with the registry
register_checker('motor', 'frame', MotorFrameCompatibilityChecker)