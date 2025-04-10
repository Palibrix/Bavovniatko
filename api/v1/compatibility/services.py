from api.v1.compatibility.checkers import get_checker
from components.models import Camera, Frame, Antenna, Motor, Propeller, Receiver, \
    FlightController, SpeedController, Transmitter, Battery


class CompatibilityService:
    """
    Service for checking compatibility between drone components.
    Implements selective and incremental compatibility checking.
    """
    # Define which component pairs need compatibility checking
    COMPATIBILITY_RELATIONSHIPS = {
        # Format: frozenset([type1, type2]): True
        # Antenna compatibility
        frozenset(['antenna_receiver', 'receiver']): True,
        frozenset(['antenna_transmitter', 'transmitter']): True,

        # Battery compatibility
        # frozenset(['battery', 'flight_controller']): True,
        frozenset(['battery', 'motor']): True,
        # frozenset(['battery', 'speed_controller']): True,
        frozenset(['battery', 'transmitter']): True,

        # Camera compatibility
        frozenset(['camera', 'frame']): True,
        frozenset(['camera', 'transmitter']): True,

        # Frame compatibility
        frozenset(['frame', 'motor']): True,
        frozenset(['frame', 'propeller']): True,
        frozenset(['frame', 'transmitter']): True,

        # FC compatibility
        frozenset(['flight_controller', 'speed_controller']): True,

        # Motor compatibility
        frozenset(['motor', 'speed_controller']): True,

        # Receiver compatibility
        frozenset(['receiver', 'flight_controller']): True,
    }

    # Map component type to model class
    COMPONENT_MODELS = {
        'camera': Camera,
        'frame': Frame,
        'motor': Motor,
        'propeller': Propeller,
        'receiver': Receiver,
        'flight_controller': FlightController,
        'speed_controller': SpeedController,
        'transmitter': Transmitter,
        'antenna_receiver': Antenna,
        'antenna_transmitter': Antenna,
        'battery': Battery
    }

    def check_compatibility(self, configuration, previous_configuration=None, previous_results=None):
        """
        Check compatibility of all components in the configuration.
        Efficiently handles component additions, removals, and changes.

        Args:
            configuration: Dict mapping component types to component IDs
            previous_configuration: Previous configuration for incremental checking
            previous_results: Previous compatibility results

        Returns:
            Dict with compatibility results
        """
        # Start with previous results or empty dict if first check
        compatibility_results = previous_results.copy() if previous_results else {}

        # Get currently valid component pairs
        current_pairs = self._get_component_pairs(configuration)

        # If this is the first check or configuration was empty, check all pairs
        if previous_configuration is None:
            # Check all current pairs
            for type1, id1, type2, id2 in current_pairs:
                component1 = self._get_component(type1, id1)
                component2 = self._get_component(type2, id2)

                pair_key = f"{type1}_{type2}"
                compatibility_results[pair_key] = self._check_pair_compatibility(
                    component1, type1, component2, type2)
        else:
            # Identify which component types have changed
            changed_component_types = set()
            for comp_type, comp_id in configuration.items():
                prev_id = previous_configuration.get(comp_type)
                if comp_id != prev_id:
                    changed_component_types.add(comp_type)

            # Filter to only check pairs with at least one changed component
            pairs_to_check = [
                pair for pair in current_pairs
                if pair[0] in changed_component_types or pair[2] in changed_component_types
            ]

            # Check compatibility for pairs that need checking
            for type1, id1, type2, id2 in pairs_to_check:
                component1 = self._get_component(type1, id1)
                component2 = self._get_component(type2, id2)

                pair_key = f"{type1}_{type2}"
                compatibility_results[pair_key] = self._check_pair_compatibility(
                    component1, type1, component2, type2)

            # Clean up results for removed components
            valid_pair_keys = set(f"{pair[0]}_{pair[2]}" for pair in current_pairs)
            keys_to_remove = [key for key in compatibility_results.keys()
                              if key not in valid_pair_keys]

            for key in keys_to_remove:
                del compatibility_results[key]

        return self._summarize_compatibility(compatibility_results)

    def _get_component_pairs(self, configuration):
        """
        Generate only component pairs that have defined compatibility relationships.
        Only includes pairs where both components are selected.
        """
        # Get components that have been selected
        selected_components = {
            comp_type: comp_id
            for comp_type, comp_id in configuration.items()
            if comp_id is not None
        }

        # If fewer than 2 components are selected, no pairs to check
        if len(selected_components) < 2:
            return []

        # Generate valid pairs that need compatibility checking
        component_pairs = []
        component_types = list(selected_components.keys())

        for i in range(len(component_types)):
            for j in range(i + 1, len(component_types)):
                type1 = component_types[i]
                type2 = component_types[j]

                # Check if this pair has a defined compatibility relationship
                pair_key = frozenset([type1, type2])
                if pair_key in self.COMPATIBILITY_RELATIONSHIPS:
                    id1 = selected_components[type1]
                    id2 = selected_components[type2]
                    component_pairs.append((type1, id1, type2, id2))

        return component_pairs

    def _get_component(self, component_type, component_id):
        """Get a component instance by type and ID"""
        model = self.COMPONENT_MODELS.get(component_type)
        if not model:
            raise ValueError(f"Unknown component type: {component_type}")

        try:
            return model.objects.get(id=component_id)
        except model.DoesNotExist:
            raise ValueError(f"Component not found: {component_type} with ID {component_id}")

    def _check_pair_compatibility(self, component1, type1, component2, type2):
        """
        Check compatibility between two components.
        Dispatches to appropriate checker based on component types.
        """
        # Sort component types for consistent checker lookup
        if type1 > type2:
            return self._check_pair_compatibility(component2, type2, component1, type1)

        # Get the appropriate checker for this component pair
        checker = get_checker(type1, type2)

        if checker:
            return checker.check_compatibility(component1, component2)
        else:
            # Default to compatible if no checker exists
            return {
                'is_compatible': True,
                'issues': []
            }

    def _summarize_compatibility(self, compatibility_results):
        """
        Summarize the overall compatibility results
        """
        all_issues = []
        is_compatible = True

        for pair_key, result in compatibility_results.items():
            if not result['is_compatible']:
                is_compatible = False
                all_issues.extend(result['issues'])

        return {
            'is_compatible': is_compatible,
            'issues': all_issues,
            'pair_results': compatibility_results
        }

    def get_compatible_components(self, component_type, configuration):
        # Get base queryset for the target component type
        component_model = self.COMPONENT_MODELS.get(component_type)
        if not component_model:
            raise ValueError(f"Unknown component type: {component_type}")

        # Start with all components
        queryset = component_model.objects.all()

        for other_type, other_id in configuration.items():
            if other_id is None:
                continue

            # Skip checking compatibility with itself
            if other_type == component_type:
                continue

            # Check if this pair has a compatibility relationship
            pair_key = frozenset([component_type, other_type])
            if pair_key not in self.COMPATIBILITY_RELATIONSHIPS:
                continue

            # Get the checker and the other component
            checker = get_checker(component_type, other_type) or get_checker(other_type, component_type)
            if not checker:
                continue

        # Check detailed compatibility for each component
        results = []

        # Process all components to include both compatible and incompatible
        for component in queryset:
            compatibility = self._check_component_compatibility(component, component_type, configuration)
            # Add to results with compatibility info
            component_data = self._serialize_component(component)
            component_data['compatibility'] = compatibility
            results.append(component_data)

        return results

    def get_compatible_components_from_queryset(self, component_type, configuration, queryset):
        """
        Get components from a pre-filtered queryset and add compatibility information.
        This allows reusing existing filter functionality.

        Args:
            component_type: Type of component to get
            configuration: Current component configuration
            queryset: Pre-filtered queryset from component views

        Returns:
            List of components with compatibility information
        """
        # Check detailed compatibility for each component
        results = []

        # Process all components to include both compatible and incompatible
        for component in queryset:
            compatibility = self._check_component_compatibility(component, component_type, configuration)
            # Add to results with compatibility info
            component_data = self._serialize_component(component)
            component_data['compatibility'] = compatibility
            results.append(component_data)

        return results

    def _check_component_compatibility(self, component, component_type, configuration):
        """Check if a specific component is compatible with the configuration"""
        # For each existing component type that has a compatibility relationship
        # with the target component, check compatibility
        issues = []
        is_compatible = True

        for existing_type, existing_id in configuration.items():
            if existing_id is None:
                continue

            # Skip checking compatibility with itself
            if existing_type == component_type:
                continue

            # Check if this pair has a compatibility relationship
            pair_key = frozenset([component_type, existing_type])
            if pair_key not in self.COMPATIBILITY_RELATIONSHIPS:
                continue

            # Get the existing component
            existing_component = self._get_component(existing_type, existing_id)

            # Check compatibility
            result = self._check_pair_compatibility(component, component_type,
                                                    existing_component, existing_type)

            if not result['is_compatible']:
                is_compatible = False
                issues.extend(result['issues'])

        return {
            'is_compatible': is_compatible,
            'issues': issues
        }

    def _serialize_component(self, component):
        """
        Serialize a component instance using proper serializers
        """
        from api.v1.components.serializers import (
            AntennaSerializer, CameraSerializer, FrameSerializer,
            MotorSerializer, PropellerSerializer, ReceiverSerializer,
            FlightControllerSerializer, SpeedControllerSerializer, TransmitterSerializer
        )

        # Map component types to serializers
        serializer_map = {
            'Camera': CameraSerializer,
            'Frame': FrameSerializer,
            'Motor': MotorSerializer,
            'Propeller': PropellerSerializer,
            'Receiver': ReceiverSerializer,
            'FlightController': FlightControllerSerializer,
            'SpeedController': SpeedControllerSerializer,
            'Transmitter': TransmitterSerializer,
            'Antenna': AntennaSerializer,
        }

        # Get the appropriate serializer for this component type
        component_type = component.__class__.__name__
        serializer_class = serializer_map.get(component_type)

        if serializer_class:
            return serializer_class(component).data

        # Fallback to basic serialization if no serializer found
        return {
            'id': component.id,
            'manufacturer': component.manufacturer,
            'model': component.model,
        }
