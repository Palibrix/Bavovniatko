from django.db.models import Q
from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.components.filters import AntennaFilter
from api.v1.components.serializers import AntennaSerializer
from components.models import Antenna


class AntennaAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = AntennaSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Antenna.objects.all().distinct()
    filterset_class = AntennaFilter
    search_fields = ['model', 'manufacturer']

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
