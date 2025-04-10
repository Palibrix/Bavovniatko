from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class FrameTransmitterCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between frame and transmitter (VTX).
    Checks if transmitter dimensions are compatible with frame's VTX mounting options.
    """

    def check_compatibility(self, frame, transmitter):
        """
        Check if transmitter is compatible with frame's VTX mounting options.

        Args:
            frame: Frame instance
            transmitter: Transmitter instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check if frame has VTX mounting dimensions
        if not frame.vtx_details.exists():
            issues.append({
                'type': 'missing_frame_vtx_mounts',
                'severity': 'warning',
                'message': 'Frame is missing VTX mount information',
                'component_refs': ['frame']
            })
            # Not a critical issue, so we'll continue and consider it compatible
        else:
            # Check transmitter dimensions compatibility
            if not hasattr(transmitter, 'length') or not hasattr(transmitter, 'height') or not hasattr(transmitter,
                                                                                                       'thickness'):
                issues.append({
                    'type': 'missing_transmitter_dimensions',
                    'severity': 'warning',
                    'message': 'Transmitter is missing dimension information',
                    'component_refs': ['transmitter']
                })
                # Not a critical issue, so we'll continue
            else:
                # Check if any frame VTX mount matches the transmitter dimensions
                # Note: Transmitter dimensions (length, height, thickness) don't directly
                # map to mounting dimensions, so we'll do an approximate check

                transmitter_length = transmitter.length
                transmitter_height = transmitter.height

                # Define a tolerance range for fitting (20% flexibility)
                tolerance = 0.2

                mount_match = False
                compatible_mounts = []

                for vtx_detail in frame.vtx_details.all():
                    vtx_height = vtx_detail.vtx_mount_height
                    vtx_width = vtx_detail.vtx_mount_width

                    # Check if transmitter dimensions are within tolerance of mount dimensions
                    # This is an approximate check
                    if ((abs(vtx_height - transmitter_height) / transmitter_height <= tolerance and
                         abs(vtx_width - transmitter_length) / transmitter_length <= tolerance) or
                            (abs(vtx_height - transmitter_length) / transmitter_length <= tolerance and
                             abs(vtx_width - transmitter_height) / transmitter_height <= tolerance)):
                        mount_match = True
                        compatible_mounts.append(f"{vtx_height}x{vtx_width}mm")

                if not mount_match:
                    # Format error message with available mounts
                    mount_options = [
                        f"{detail.vtx_mount_height}x{detail.vtx_mount_width}mm"
                        for detail in frame.vtx_details.all()
                    ]
                    mount_options_str = ", ".join(mount_options)

                    issues.append({
                        'type': 'vtx_mount_mismatch',
                        'severity': 'important',  # Not critical, but important
                        'message': f"Transmitter dimensions ({transmitter_length}x{transmitter_height}mm) may not fit properly on frame VTX mounts ({mount_options_str})",
                        'component_refs': ['transmitter', 'frame']
                    })
                elif compatible_mounts:
                    # Add an informational message about which mounts are compatible
                    issues.append({
                        'type': 'vtx_mount_info',
                        'severity': 'info',
                        'message': f"Transmitter is compatible with frame VTX mounts: {', '.join(compatible_mounts)}",
                        'component_refs': ['transmitter', 'frame']
                    })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'frame' or 'transmitter'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'frame' and hasattr(other_component, 'length') and hasattr(other_component, 'height'):
            # Filtering frames based on transmitter
            transmitter = other_component
            return {
                'transmitter_length': transmitter.length,
                'transmitter_height': transmitter.height
            }

        elif component_type == 'transmitter' and hasattr(other_component, 'vtx_details'):
            # Filtering transmitters based on frame
            frame = other_component

            if frame.vtx_details.exists():
                # Get all frame VTX mount dimensions
                mount_dimensions = []
                for detail in frame.vtx_details.all():
                    mount_dimensions.append((detail.vtx_mount_height, detail.vtx_mount_width))

                return {'mount_dimensions': mount_dimensions}

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'frame' or 'transmitter'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        # For this checker, we won't apply strict filtering since the compatibility
        # is based on approximate matching with tolerance, which is hard to express
        # in a database query. Instead, we'll return the unfiltered queryset and
        # let the detailed compatibility check handle it.
        return queryset


# Register this checker with the registry
register_checker('frame', 'transmitter', FrameTransmitterCompatibilityChecker)