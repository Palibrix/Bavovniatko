from rest_framework import status
from rest_framework.decorators import action
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from django.db.models import Count, Min, Max
from django_filters.rest_framework import FilterSet


class MetadataFilterSet(FilterSet):
    """
    Extended FilterSet with metadata about filter UI structure.
    Provides methods to get filter options and counts for faceted search.
    """
    # Will be overridden by subclasses to define UI structure
    filter_metadata = {}

    @classmethod
    def get_filter_metadata(cls):
        """Return filter UI metadata structure"""
        return cls.filter_metadata

    @classmethod
    def get_filter_options(cls, queryset, search_term=None, filter_id=None):
        """
        Return filter metadata with option counts for each filter.

        This enhances the metadata with actual data from the database:
        - Range filters include min/max values
        - Choice filters include all available options with counts

        Args:
            queryset: Base queryset for counting
            search_term: Optional search term to filter options (for choice filters)
            filter_id: Optional specific filter ID to return options for
        """
        # Get specific filter if requested
        if filter_id:
            for group in cls.filter_metadata.get('groups', []):
                for filter_def in group.get('filters', []):
                    if filter_def.get('id') == filter_id:
                        field_name = filter_def.get('field')
                        filter_type = filter_def.get('type')
                        model_field = filter_def.get('model_field', None)

                        if not field_name:
                            return {"error": "Filter has no field defined"}

                        if filter_type == 'range':
                            return {
                                'filter_id': filter_id,
                                'type': 'range',
                                'options': cls._get_range_boundaries(queryset, field_name)
                            }
                        elif filter_type == 'choice':
                            return {
                                'filter_id': filter_id,
                                'type': 'choice',
                                'options': cls._get_choice_options(
                                    queryset,
                                    field_name,
                                    model_field,
                                    search_term
                                )
                            }

            return {"error": f"Filter '{filter_id}' not found"}

        # Deep copy to avoid modifying the original class attribute
        import copy
        metadata = copy.deepcopy(cls.filter_metadata)

        # Populate option counts for each filter
        for group in metadata.get('groups', []):
            for filter_def in group.get('filters', []):
                filter_type = filter_def.get('type')
                field_name = filter_def.get('field')

                if not field_name:
                    continue

                if filter_type == 'range':
                    filter_def.update(cls._get_range_boundaries(queryset, field_name))

                elif filter_type == 'choice':
                    # Get options with counts for choice filters
                    filter_def['options'] = cls._get_choice_options(
                        queryset,
                        field_name,
                        filter_def.get('model_field', None),
                        search_term
                    )

        return metadata

    @staticmethod
    def _get_range_boundaries(queryset, field_name):
        """Get min/max values for a numeric field"""
        # Handle nested fields
        field_path = field_name

        result = queryset.aggregate(
            min_value=Min(field_path),
            max_value=Max(field_path)
        )

        return {
            'min': result['min_value'],
            'max': result['max_value'],
        }

    @staticmethod
    def _get_choice_options(queryset, field_name, model_field=None, search_term=None):
        """
        Get available options with counts for a choice filter

        Args:
            queryset: Base queryset
            field_name: Filter field name (can include relations using __)
            model_field: For M2M or ForeignKey, the field in related model to use for display
            search_term: Optional search term to filter options
        """
        options = []

        # Direct field (no relation)
        if '__' not in field_name:
            counts = (
                queryset
                .values(field_name)
                .annotate(count=Count('id'))
                .order_by('-count')
            )

            options = [
                {
                    'value': item[field_name],
                    'display': item[field_name],
                    'count': item['count']
                } for item in counts if item[field_name] is not None
            ]

        # Related field (with double underscore)
        else:
            parts = field_name.split('__')

            # Special case for M2M relations
            if parts[-1] == 'type' and len(parts) == 2:
                # This is likely a relation like 'antenna_connectors__type'
                relation = parts[0]
                relation_field = parts[1]

                # For M2M, we need to use the through model
                related_model = queryset.model._meta.get_field(relation).related_model

                # Get all values from the related model
                all_options = related_model.objects.all()

                options = []
                for option in all_options:
                    # Count how many items in the queryset have this option
                    option_value = getattr(option, relation_field)
                    count = queryset.filter(**{field_name: option_value}).count()

                    if model_field:
                        display_value = getattr(option, model_field)
                    else:
                        display_value = str(option)

                    options.append({
                        'value': option_value,
                        'display': display_value,
                        'count': count
                    })

            else:
                # Standard relation (ForeignKey)
                # Get unique values through the relation
                counts = (
                    queryset
                    .values(field_name)
                    .annotate(count=Count('id', distinct=True))
                    .order_by('-count')
                )

                options = [
                    {
                        'value': item[field_name],
                        'display': item[field_name],
                        'count': item['count']
                    } for item in counts if item[field_name] is not None
                ]

        # Apply search filter if provided
        if search_term and options:
            search_term = search_term.lower()
            options = [
                opt for opt in options
                if search_term in str(opt['display']).lower()
            ]

        return options


class SuggestionActionsMixin:

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        try:
            instance.accept()
            return Response({'message': 'Suggestion accepted'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        try:
            admin_comment = request.data.get('admin_comment')
            instance.deny(admin_comment=admin_comment)
            return Response({'message': 'Suggestion denied'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.status == 'approved':
            raise ValidationError("Cannot modify approved suggestion")

        # If denied suggestion is being modified, set it back to pending
        if instance.status == 'denied':
            serializer.save(status='pending')
        else:
            serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')
