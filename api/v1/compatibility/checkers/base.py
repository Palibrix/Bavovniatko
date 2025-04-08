"""
Base class for compatibility checkers.
"""

from abc import ABC, abstractmethod


class BaseCompatibilityChecker(ABC):
    """
    Base class for all compatibility checkers.

    Each checker is responsible for determining compatibility between a pair of components
    and providing filtering parameters to efficiently query compatible components.
    """

    @abstractmethod
    def check_compatibility(self, component1, component2):
        """
        Check if the two components are compatible.

        Args:
            component1: First component instance
            component2: Second component instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        pass

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters to efficiently query compatible components.

        Args:
            component_type: Type of component being filtered ('camera', 'frame', etc.)
            other_component: The other component instance to filter against

        Returns:
            dict: Filter parameters specific to this component pair
        """
        # Default implementation returns no filters
        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to the queryset.

        Args:
            component_type: Type of component being filtered
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        # Default implementation returns queryset unchanged
        return queryset