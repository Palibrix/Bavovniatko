from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.compatibility.serializers import (
    ConfigurationCheckSerializer,
    ConfigurationSerializer
)
from api.v1.compatibility.services import CompatibilityService


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

        # Get compatible components using service
        compatibility_service = CompatibilityService()
        results = compatibility_service.get_compatible_components(
            component_type, configuration
        )

        return Response(results)