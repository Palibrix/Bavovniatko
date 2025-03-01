from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from api.v1.lists.serializers import (
    ListOverviewSerializer, ListDetailSerializer,
    AddComponentSerializer, RemoveComponentSerializer,
    ComponentItemSerializer
)
from lists.models import List
from lists.registry import ComponentRegistry


class ListViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user's lists of components.
    Provides CRUD operations and custom actions for managing list items.
    """
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['name', 'description']

    def get_queryset(self):
        """Return only lists owned by the current user."""
        return List.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Return the appropriate serializer based on the action."""
        if self.action == 'retrieve':
            return ListDetailSerializer
        return ListOverviewSerializer

    def perform_create(self, serializer):
        """Create a new list with the current user as owner."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_component(self, request, pk=None):
        """Add a component to the list."""
        list_obj = self.get_object()
        serializer = AddComponentSerializer(data=request.data)

        if serializer.is_valid():
            component_type = serializer.validated_data['component_type']
            component = serializer.validated_data['component']

            # Check if the component is already in the list
            related_name = f"{component_type}_items"
            if hasattr(list_obj, related_name):
                items = getattr(list_obj, related_name)
                if items.filter(component=component).exists():
                    return Response(
                        {"detail": _("This component is already in the list.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Get the model class for this component type
            item_model = ComponentRegistry.get_model(component_type)
            if not item_model:
                return Response(
                    {"detail": _("Invalid component type: {0}").format(component_type)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new list item
            item_model.objects.create(list=list_obj, component=component)

            return Response(
                {"detail": _("Component added to list successfully.")},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_components(self, request, pk=None):
        """Remove one or more components from the list."""
        list_obj = self.get_object()
        serializer = RemoveComponentSerializer(data=request.data)

        if serializer.is_valid():
            # Check if we're doing single or bulk removal
            if 'items' in serializer.validated_data:
                # Bulk removal
                items = serializer.validated_data['items']
                removed = list_obj.remove_items_bulk(items)
                return Response(
                    {"detail": _("Removed {0} components from the list.").format(removed)},
                    status=status.HTTP_200_OK
                )
            else:
                # Single component removal
                component_type = serializer.validated_data['component_type']
                component_id = serializer.validated_data['component_id']

                # Check if the component exists in the list
                related_name = f"{component_type}_items"
                if not hasattr(list_obj, related_name):
                    return Response(
                        {"detail": _("Invalid component type: {0}").format(component_type)},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                items = getattr(list_obj, related_name)
                result = items.filter(component_id=component_id).delete()

                if result[0] == 0:
                    return Response(
                        {"detail": _("Component not found in the list.")},
                        status=status.HTTP_404_NOT_FOUND
                    )

                return Response(
                    {"detail": _("Component removed from the list.")},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def filter_by_type(self, request, pk=None):
        """Get list items filtered by component type."""
        list_obj = self.get_object()
        component_type = request.query_params.get('type')

        if not component_type or component_type not in ComponentRegistry.get_all_types():
            return Response(
                {"detail": _("Invalid or missing component type parameter.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        related_name = f"{component_type}_items"
        if not hasattr(list_obj, related_name):
            return Response([])

        items = getattr(list_obj, related_name).select_related('component').all()

        # Add component type info to items for serializer
        for item in items:
            item.component_type = component_type
            item.component_id = item.component.id

        # Sort by added_at
        items = sorted(items, key=lambda x: x.added_at, reverse=True)

        serializer = ComponentItemSerializer(items, many=True)
        return Response(serializer.data)