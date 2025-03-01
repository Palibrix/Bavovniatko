from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from api.v1.users.serializers import UserSerializer
from lists.models import List
from lists.registry import ComponentRegistry
from components.models import (
    Antenna, Camera, Frame, Motor, Propeller,
    Receiver, Stack, FlightController, SpeedController, Transmitter
)


class ListOverviewSerializer(serializers.ModelSerializer):
    """
    Serializer for list overview - used in list listings.
    Provides basic information about the list.
    """
    owner = UserSerializer(read_only=True)
    parts_count = serializers.IntegerField(source='count_all', read_only=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'updated_at', 'parts_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']


class ComponentItemSerializer(serializers.Serializer):
    """
    Serializer for any component item in a list.
    Used as part of ListDetailSerializer to provide a unified representation
    of different component types.
    """
    id = serializers.IntegerField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    component_id = serializers.IntegerField(read_only=True)
    display_name = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    added_at = serializers.DateTimeField(read_only=True)

    def get_display_name(self, obj):
        """Return the string representation of the component"""
        if hasattr(obj, 'component'):
            return str(obj.component)
        return "Unknown Component"

    def get_image_url(self, obj):
        """Return the image with lowest order or order=0 if available"""
        if hasattr(obj, 'component') and hasattr(obj.component, 'images'):
            images = obj.component.images.filter(accepted=True)

            if not images.exists():
                return None

            # Try to get the image with order=0 first
            zero_ordered = images.filter(order=0).first()
            if zero_ordered:
                return zero_ordered.image.url

            # Otherwise get the image with the lowest order value
            lowest_ordered = images.order_by('order').first()
            if lowest_ordered:
                return lowest_ordered.image.url

        return None


class ListDetailSerializer(ListOverviewSerializer):
    """
    Detailed serializer for lists, including all items.
    Used for the detail view of a list.
    """
    items = serializers.SerializerMethodField()
    parts_count_by_type = serializers.SerializerMethodField()

    class Meta(ListOverviewSerializer.Meta):
        fields = ListOverviewSerializer.Meta.fields + ['items', 'parts_count_by_type']

    def get_items(self, obj):
        """Get all items in the list with their component details"""
        # Get items with component type information
        all_items = []

        for component_type in ComponentRegistry.get_all_types():
            related_name = f"{component_type}_items"
            if not hasattr(obj, related_name):
                continue

            component_items = getattr(obj, related_name).select_related('component').prefetch_related(
                'component__images'
            ).all()

            for item in component_items:
                # Add component type information
                item.component_type = component_type
                item.component_id = item.component.id
                all_items.append(item)

        # Sort by added_at (newest first)
        sorted_items = sorted(all_items, key=lambda x: x.added_at, reverse=True)

        # Apply pagination if requested in query params
        return ComponentItemSerializer(sorted_items, many=True).data

    def get_parts_count_by_type(self, obj):
        """Get count of parts by component type"""
        return obj.count_by_type()


class AddComponentSerializer(serializers.Serializer):
    """
    Serializer for adding a component to a list.
    Validates that the component exists and isn't already in the list.
    """
    component_type = serializers.ChoiceField(choices=[
        ('antenna', _('Antenna')),
        ('camera', _('Camera')),
        ('frame', _('Frame')),
        ('motor', _('Motor')),
        ('propeller', _('Propeller')),
        ('receiver', _('Receiver')),
        ('stack', _('Stack')),
        ('flight_controller', _('Flight Controller')),
        ('speed_controller', _('Speed Controller')),
        ('transmitter', _('Transmitter')),
    ])
    component_id = serializers.IntegerField(min_value=1)

    def validate(self, data):
        """Validate the component exists"""
        component_type = data['component_type']
        component_id = data['component_id']

        # Map component types to models
        model_map = {
            'antenna': Antenna,
            'camera': Camera,
            'frame': Frame,
            'motor': Motor,
            'propeller': Propeller,
            'receiver': Receiver,
            'stack': Stack,
            'flight_controller': FlightController,
            'speed_controller': SpeedController,
            'transmitter': Transmitter,
        }

        model_class = model_map.get(component_type)
        if not model_class:
            raise serializers.ValidationError(
                _("Invalid component type: {0}").format(component_type)
            )

        try:
            component = model_class.objects.get(pk=component_id)
            # Store the actual component in validated data
            data['component'] = component
        except model_class.DoesNotExist:
            raise serializers.ValidationError(
                _("{0} with ID {1} does not exist").format(
                    component_type.replace('_', ' ').title(), component_id
                )
            )

        return data


class RemoveComponentSerializer(serializers.Serializer):
    """
    Serializer for removing components from a list.
    Accepts a single component or multiple components.
    """
    # For single component removal
    component_type = serializers.CharField(required=False)
    component_id = serializers.IntegerField(required=False, min_value=1)

    # For bulk removal
    items = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    def validate(self, data):
        """Validate either a single component or multiple items are provided"""
        # Check if we have single component data
        has_single = 'component_type' in data and 'component_id' in data

        # Check if we have bulk items data
        has_bulk = 'items' in data and data['items']

        if not has_single and not has_bulk:
            raise serializers.ValidationError(
                _("Must provide either component_type and component_id, or items list")
            )

        # If we have single component data, validate types
        if has_single:
            if data['component_type'] not in ComponentRegistry.get_all_types():
                raise serializers.ValidationError(
                    _("Invalid component type: {0}").format(data['component_type'])
                )

        # If we have bulk items, validate each item
        if has_bulk:
            validated_items = []
            for item in data['items']:
                component_type = item.get('component_type')
                component_id = item.get('component_id')

                if not component_type or not component_id:
                    continue

                if component_type not in ComponentRegistry.get_all_types():
                    continue

                validated_items.append({
                    'component_type': component_type,
                    'component_id': component_id
                })

            # Replace with validated items
            data['items'] = validated_items

        return data