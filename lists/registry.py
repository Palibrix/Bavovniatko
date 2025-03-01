class ComponentRegistry:
    """Registry for keeping track of component types and their list item models."""
    _registry = {}

    @classmethod
    def register(cls, component_type, item_model):
        """Register a new component type with its corresponding list item model."""
        cls._registry[component_type] = item_model

    @classmethod
    def get_model(cls, component_type):
        """Get the list item model for a given component type."""
        return cls._registry.get(component_type)

    @classmethod
    def get_all_types(cls):
        """Get all registered component types."""
        return list(cls._registry.keys())

    @classmethod
    def get_all_models(cls):
        """Get all registered list item models."""
        return list(cls._registry.values())
