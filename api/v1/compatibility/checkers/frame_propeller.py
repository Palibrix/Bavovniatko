from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class FramePropellerCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between frame and propeller.
    Checks if propeller size matches frame's supported propeller size.
    """

    def check_compatibility(self, frame, propeller):
        issues = []

        # Check propeller size compatibility
        if not hasattr(frame, 'prop_size'):
            issues.append({
                'type': 'missing_frame_prop_size',
                'severity': 'critical',
                'message': 'Frame is missing propeller size information',
                'component_refs': ['frame']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        if not hasattr(propeller, 'size'):
            issues.append({
                'type': 'missing_propeller_size',
                'severity': 'critical',
                'message': 'Propeller is missing size information',
                'component_refs': ['propeller']
            })
            return {
                'is_compatible': False,
                'issues': issues
            }

        # Convert sizes to comparable format
        frame_prop_size = frame.prop_size
        propeller_size = str(propeller.size)

        # Check if sizes match (this might need more complex logic depending on how sizes are stored)
        # For example, frame might support a range of prop sizes
        if frame_prop_size != propeller_size:
            # Try to handle different formats (e.g., "5 inch" vs "5")
            frame_prop_numeric = ''.join(filter(str.isdigit, frame_prop_size))
            propeller_numeric = ''.join(filter(str.isdigit, propeller_size))

            if frame_prop_numeric != propeller_numeric:
                issues.append({
                    'type': 'propeller_size_mismatch',
                    'severity': 'critical',
                    'message': f"Propeller size ({propeller_size}) doesn't match frame's supported propeller size ({frame_prop_size})",
                    'component_refs': ['propeller', 'frame']
                })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'frame' or 'propeller'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'frame' and hasattr(other_component, 'size'):
            # Filtering frames based on propeller
            propeller = other_component
            return {
                'prop_size': str(propeller.size)
            }

        elif component_type == 'propeller' and hasattr(other_component, 'prop_size'):
            # Filtering propellers based on frame
            frame = other_component
            return {
                'frame_prop_size': frame.prop_size
            }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'frame' or 'propeller'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'frame':
            # Filtering frames
            if 'prop_size' in filter_params:
                prop_size = filter_params['prop_size']

                # Try exact match first
                matches = queryset.filter(prop_size=prop_size)
                if matches.exists():
                    return matches

                # If no exact match, try numeric comparison
                prop_numeric = ''.join(filter(str.isdigit, prop_size))

                # This is a bit complex as it requires string manipulation in the database
                # For simplicity, we'll filter in Python instead of using a complex query
                # This is less efficient but should work
                numeric_matches = []
                for frame in queryset:
                    frame_prop_numeric = ''.join(filter(str.isdigit, frame.prop_size))
                    if frame_prop_numeric == prop_numeric:
                        numeric_matches.append(frame.id)

                if numeric_matches:
                    return queryset.filter(id__in=numeric_matches)

        elif component_type == 'propeller':
            # Filtering propellers
            if 'frame_prop_size' in filter_params:
                frame_prop_size = filter_params['frame_prop_size']

                # Try exact match first
                matches = queryset.filter(size=frame_prop_size)
                if matches.exists():
                    return matches

                # If no exact match, try numeric comparison
                frame_prop_numeric = ''.join(filter(str.isdigit, frame_prop_size))

                # Convert propeller size to string for comparison
                numeric_matches = []
                for propeller in queryset:
                    prop_numeric = ''.join(filter(str.isdigit, str(propeller.size)))
                    if prop_numeric == frame_prop_numeric:
                        numeric_matches.append(propeller.id)

                if numeric_matches:
                    return queryset.filter(id__in=numeric_matches)

        return queryset


# Register this checker with the registry
register_checker('frame', 'propeller', FramePropellerCompatibilityChecker)