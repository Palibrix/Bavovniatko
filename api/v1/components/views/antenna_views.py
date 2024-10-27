from django.db.models import Q
from rest_framework import mixins, viewsets, filters
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
