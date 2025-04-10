from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.compatibility.serializers import (
    ConfigurationCheckSerializer,
    ConfigurationSerializer
)
from api.v1.compatibility.services import CompatibilityService
from api.v1.components.filters import AntennaFilter, MotorFilter, FrameFilter, CameraFilter, PropellerFilter, \
    TransmitterFilter, FlightControllerFilter, SpeedControllerFilter, ReceiverFilter
from api.v1.components.views import AntennaAPIViewSet, MotorAPIViewSet, CameraAPIViewSet, FrameAPIViewSet, \
    PropellerAPIViewSet, TransmitterAPIViewSet, ReceiverAPIViewSet, SpeedControllerAPIViewSet, \
    FlightControllerAPIViewSet


class CompatibilityCheckView(APIView):
    """
    Check compatibility of a drone configuration
    """

    def post(self, request):
        """
        Check compatibility of the configuration in the request
        """
        # Validate the configuration format
        serializer = ConfigurationCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the configuration and optional previous state
        configuration = serializer.validated_data.get('configuration', {})
        previous_configuration = serializer.validated_data.get('previous_configuration')
        previous_results = serializer.validated_data.get('previous_results')

        # Check compatibility using service
        compatibility_service = CompatibilityService()
        compatibility_results = compatibility_service.check_compatibility(
            configuration, previous_configuration, previous_results
        )

        return Response(compatibility_results)


class CompatibleComponentsView(APIView):
    """
    Get components compatible with current drone configuration
    """

    def post(self, request, component_type):
        """
        Get compatible components based on configuration
        """
        # Validate the configuration format
        serializer = ConfigurationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the configuration from request
        configuration = serializer.validated_data.get('configuration', {})

        # Map component types to view classes and filter classes
        viewset_map = {
            'antenna_receiver': (AntennaAPIViewSet, AntennaFilter),
            'antenna_transmitter': (AntennaAPIViewSet, AntennaFilter),
            'camera': (CameraAPIViewSet, CameraFilter),
            'frame': (FrameAPIViewSet, FrameFilter),
            'motor': (MotorAPIViewSet, MotorFilter),
            'propeller': (PropellerAPIViewSet, PropellerFilter),
            'transmitter': (TransmitterAPIViewSet, TransmitterFilter),
            'flight_controller': (FlightControllerAPIViewSet, FlightControllerFilter),
            'speed_controller': (SpeedControllerAPIViewSet, SpeedControllerFilter),
            'receiver': (ReceiverAPIViewSet, ReceiverFilter),
        }

        # Get compatible components using service
        compatibility_service = CompatibilityService()

        # Get the appropriate viewset and filter class
        if component_type in viewset_map:
            ViewSetClass, FilterClass = viewset_map[component_type]

            # Initialize the viewset
            viewset = ViewSetClass()
            viewset.request = request
            viewset.format_kwarg = None

            # Get the queryset with filters applied
            queryset = viewset.filter_queryset(viewset.get_queryset())

            # Apply compatibility filtering
            results = compatibility_service.get_compatible_components_from_queryset(
                component_type, configuration, queryset
            )

            return Response(results)

        else:
            # For component types without specific handling, use the basic function
            results = compatibility_service.get_compatible_components(
                component_type, configuration
            )

            return Response(results)
