from django.apps import AppConfig


class ListsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lists'
    verbose_name = 'Part Lists'

    def ready(self):
        # Import and register all list item models
        from .registry import ComponentRegistry
        from .models import (
            AntennaListItem, CameraListItem, FrameListItem, MotorListItem,
            PropellerListItem, ReceiverListItem, StackListItem,
            FlightControllerListItem, SpeedControllerListItem, TransmitterListItem
        )

        # Register each component type with its list item model
        ComponentRegistry.register('antenna', AntennaListItem)
        ComponentRegistry.register('camera', CameraListItem)
        ComponentRegistry.register('frame', FrameListItem)
        ComponentRegistry.register('motor', MotorListItem)
        ComponentRegistry.register('propeller', PropellerListItem)
        ComponentRegistry.register('receiver', ReceiverListItem)
        ComponentRegistry.register('stack', StackListItem)
        ComponentRegistry.register('flight_controller', FlightControllerListItem)
        ComponentRegistry.register('speed_controller', SpeedControllerListItem)
        ComponentRegistry.register('transmitter', TransmitterListItem)
