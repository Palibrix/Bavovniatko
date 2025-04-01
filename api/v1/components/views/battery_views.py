from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from api.v1.components.filters import BatteryFilter
from api.v1.components.mixins import BaseComponentFilterMixin
from api.v1.components.serializers.battery_serializers import BatterySerializer, BatteryWriteSerializer
from components.models import Battery


class BatteryAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin, mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Battery.objects.all().distinct()
    # filterset_class = BatteryFilter
    # search_fields = ['model', 'manufacturer', 'size', 'connector_type']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BatteryWriteSerializer
        return BatterySerializer