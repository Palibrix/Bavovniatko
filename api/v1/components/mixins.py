from rest_framework.decorators import action
from rest_framework.response import Response

class BaseComponentFilterMixin:
    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """
        Return filter options with counts for faceted search.
        This provides the structure and available filter options.

        Query parameters:
        - filter_id: (string) Optional specific filter to get options for
        - search: (string) Optional search term to filter options
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Get query parameters
        filter_id = request.query_params.get('filter_id', None)
        search_term = request.query_params.get('search', None)

        # Get complete or specific filter options
        metadata = self.filterset_class.get_filter_options(
            queryset,
            search_term=search_term,
            filter_id=filter_id
        )

        return Response(metadata)