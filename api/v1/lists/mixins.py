class ComponentMixin:
    """
    Mixin that provides component serialization methods.
    """

    @classmethod
    def get_component_model(cls, component_type):
        """Get the model class for a given component type"""
        from django.apps import apps
        return apps.get_model('components', component_type.capitalize())

    @classmethod
    def get_component_serializer(cls, component_type):
        """Get the appropriate serializer for a component type"""
        # Import all component serializers dynamically
        from api.v1.components.serializers import (
            AntennaSerializer, CameraSerializer, MotorSerializer,
            FrameSerializer, ReceiverSerializer,
            TransmitterSerializer, FlightControllerSerializer,
            SpeedControllerSerializer, PropellerSerializer,
            StackSerializer
        )

        # Map component types to their serializers
        serializer_map = {
            'antenna': AntennaSerializer,
            'camera': CameraSerializer,
            'motor': MotorSerializer,
            'frame': FrameSerializer,
            'receiver': ReceiverSerializer,
            'transmitter': TransmitterSerializer,
            'flight_controller': FlightControllerSerializer,
            'speed_controller': SpeedControllerSerializer,
            'propeller': PropellerSerializer,
            'stack': StackSerializer
        }

        return serializer_map.get(component_type.lower())

    @classmethod
    def get_item_model(cls, component_type):
        """Get the list item model for a component type"""
        from django.apps import apps
        model_name = f"{component_type.capitalize()}ListItem"
        return apps.get_model('favorites', model_name)