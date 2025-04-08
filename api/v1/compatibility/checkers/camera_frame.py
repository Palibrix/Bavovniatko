"""
Camera-Frame compatibility checker.
"""

from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class CameraFrameCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between camera and frame components.
    Checks if camera dimensions match any frame camera mount dimensions.
    """

    def check_compatibility(self, camera, frame):
        """
        Check if the camera is compatible with the frame.

        A camera is compatible with a frame if its dimensions match
        any of the frame's camera mount dimensions.

        Args:
            camera: Camera instance
            frame: Frame instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check if camera can fit in any of the frame's camera mounts
        camera_compatible = False

        # Get all camera dimensions
        if not camera.details.exists():
            issues.append({
                'type': 'missing_details',
                'severity': 'critical',
                'message': 'Camera has no dimension details',
                'component_refs': ['camera']
            })
            return {'is_compatible': False, 'issues': issues}

        if not frame.camera_details.exists():
            issues.append({
                'type': 'missing_details',
                'severity': 'critical',
                'message': 'Frame has no camera mount details',
                'component_refs': ['frame']
            })
            return {'is_compatible': False, 'issues': issues}

        # Check each camera detail against each frame camera mount
        for camera_detail in camera.details.all():
            for frame_camera_detail in frame.camera_details.all():
                if (camera_detail.height == frame_camera_detail.camera_mount_height and
                        camera_detail.width == frame_camera_detail.camera_mount_width):
                    camera_compatible = True
                    break

            if camera_compatible:
                break

        if not camera_compatible:
            camera_sizes = [f"{detail.height}x{detail.width}mm" for detail in camera.details.all()]
            frame_sizes = [f"{detail.camera_mount_height}x{detail.camera_mount_width}mm"
                           for detail in frame.camera_details.all()]

            issues.append({
                'type': 'dimension_mismatch',
                'severity': 'critical',
                'message': f"Camera dimensions ({', '.join(camera_sizes)}) don't match any frame "
                          f"camera mount dimensions ({', '.join(frame_sizes)})",
                'component_refs': ['camera', 'frame']
            })

        return {
            'is_compatible': camera_compatible,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for camera or frame based on the other component.

        Args:
            component_type: Either 'camera' or 'frame'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'camera' and hasattr(other_component, 'camera_details'):
            # Filtering cameras based on frame
            frame = other_component
            if frame.camera_details.exists():
                # Build a complex Q query to match any of the frame's camera mount dimensions
                mount_q = Q()
                for mount in frame.camera_details.all():
                    mount_q |= Q(details__height=mount.camera_mount_height,
                               details__width=mount.camera_mount_width)

                return {'mount_dimensions_q': mount_q}

        elif component_type == 'frame' and hasattr(other_component, 'details'):
            # Filtering frames based on camera
            camera = other_component
            if camera.details.exists():
                # Build a complex Q query to match any of the camera's dimensions
                camera_q = Q()
                for detail in camera.details.all():
                    camera_q |= Q(camera_details__camera_mount_height=detail.height,
                                camera_details__camera_mount_width=detail.width)

                return {'camera_dimensions_q': camera_q}

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply camera or frame filter parameters to the queryset.

        Args:
            component_type: Either 'camera' or 'frame'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'camera' and 'mount_dimensions_q' in filter_params:
            return queryset.filter(filter_params['mount_dimensions_q']).distinct()

        elif component_type == 'frame' and 'camera_dimensions_q' in filter_params:
            return queryset.filter(filter_params['camera_dimensions_q']).distinct()

        return queryset


# Register this checker with the registry
register_checker('camera', 'frame', CameraFrameCompatibilityChecker)