from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from api.v1.builds.filters import DroneFilter
from api.v1.builds.serializers import DroneSerializer
from builds.models import Drone


class DroneAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = DroneSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Drone.objects.all().distinct()
    filterset_class = DroneFilter
    search_fields = ['model', 'manufacturer']
