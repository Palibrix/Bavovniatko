from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class CameraTransmitterCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between camera and transmitter.
    Checks:
    1. Video format compatibility - Camera video formats must match transmitter formats
    2. Signal type compatibility - Camera output type must be compatible with transmitter input
    """

    def check_compatibility(self, camera, transmitter):
        """
        Check if camera is compatible with transmitter.

        Args:
            camera: Camera instance
            transmitter: Transmitter instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check 1: Video format compatibility
        if not camera.video_formats.exists():
            issues.append({
                'type': 'missing_camera_formats',
                'severity': 'critical',
                'message': 'Camera is missing video format information',
                'component_refs': ['camera']
            })
        elif not transmitter.video_formats.exists():
            issues.append({
                'type': 'missing_transmitter_formats',
                'severity': 'critical',
                'message': 'Transmitter is missing video format information',
                'component_refs': ['transmitter']
            })
        else:
            # Check if there are common video formats
            camera_formats = set(format_obj.id for format_obj in camera.video_formats.all())
            transmitter_formats = set(format_obj.id for format_obj in transmitter.video_formats.all())

            if not camera_formats.intersection(transmitter_formats):
                # Get format names for error message
                camera_format_names = [format_obj.format for format_obj in camera.video_formats.all()]
                transmitter_format_names = [format_obj.format for format_obj in transmitter.video_formats.all()]

                issues.append({
                    'type': 'video_format_mismatch',
                    'severity': 'critical',
                    'message': f"Camera video formats ({', '.join(camera_format_names)}) incompatible with transmitter formats ({', '.join(transmitter_format_names)})",
                    'component_refs': ['camera', 'transmitter']
                })

        # Check 2: Signal type compatibility
        if not hasattr(camera, 'output_type'):
            issues.append({
                'type': 'missing_camera_output_type',
                'severity': 'critical',
                'message': 'Camera is missing output type information',
                'component_refs': ['camera']
            })
        elif not hasattr(transmitter, 'output'):
            issues.append({
                'type': 'missing_transmitter_input_type',
                'severity': 'critical',
                'message': 'Transmitter is missing input type information',
                'component_refs': ['transmitter']
            })
        else:
            camera_output = camera.output_type
            transmitter_input = transmitter.output  # Assuming this is the input type field

            # Check signal compatibility (assuming A=Analog, D=Digital)
            if camera_output != transmitter_input:
                issues.append({
                    'type': 'signal_type_mismatch',
                    'severity': 'critical',
                    'message': f"Camera output type ({camera_output}) incompatible with transmitter input type ({transmitter_input})",
                    'component_refs': ['camera', 'transmitter']
                })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'camera' or 'transmitter'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'camera' and hasattr(other_component, 'video_formats') and hasattr(other_component,
                                                                                                'output'):
            # Filtering cameras based on transmitter
            transmitter = other_component

            # Get video formats
            format_ids = None
            if transmitter.video_formats.exists():
                format_ids = list(transmitter.video_formats.values_list('id', flat=True))

            # Get signal type
            signal_type = transmitter.output

            return {
                'format_ids': format_ids,
                'signal_type': signal_type
            }

        elif component_type == 'transmitter' and hasattr(other_component, 'video_formats') and hasattr(other_component,
                                                                                                       'output_type'):
            # Filtering transmitters based on camera
            camera = other_component

            # Get video formats
            format_ids = None
            if camera.video_formats.exists():
                format_ids = list(camera.video_formats.values_list('id', flat=True))

            # Get signal type
            signal_type = camera.output_type

            return {
                'format_ids': format_ids,
                'signal_type': signal_type
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'camera' or 'transmitter'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'camera':
            # Filtering cameras
            if 'format_ids' in filter_params and filter_params['format_ids']:
                format_ids = filter_params['format_ids']
                queryset = queryset.filter(video_formats__id__in=format_ids)

            if 'signal_type' in filter_params and filter_params['signal_type']:
                signal_type = filter_params['signal_type']
                queryset = queryset.filter(output_type=signal_type)

        elif component_type == 'transmitter':
            # Filtering transmitters
            if 'format_ids' in filter_params and filter_params['format_ids']:
                format_ids = filter_params['format_ids']
                queryset = queryset.filter(video_formats__id__in=format_ids)

            if 'signal_type' in filter_params and filter_params['signal_type']:
                signal_type = filter_params['signal_type']
                queryset = queryset.filter(output=signal_type)

        return queryset.distinct()


# Register this checker with the registry
register_checker('camera', 'transmitter', CameraTransmitterCompatibilityChecker)