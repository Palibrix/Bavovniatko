from django.db.models import Q
from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.components.serializers import AntennaSerializer
from components.models import Antenna


class AntennaAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = AntennaSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Antenna.objects.all()
    filterset_fields = ['manufacturer', 'center_frequency', 'bandwidth_min', 'bandwidth_max',
                        'swr', 'gain', 'radiation',
                        'type__type', 'type__direction', 'type__polarization',
                        'details__connector_type__type', 'details__angle_type']
    search_fields = ['model', 'manufacturer']
