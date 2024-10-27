from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from api.v1.components.filters import FlightControllerFilter, SpeedControllerFilter, StackFilter
from api.v1.components.serializers import StackSerializer, FlightControllerSerializer, SpeedControllerSerializer
from components.models import Receiver, Stack, FlightController, SpeedController


class StackAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = StackSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Stack.objects.all().distinct()
    filterset_class = StackFilter
    search_fields = ['model', 'manufacturer',
                     'flight_controller__model', 'flight_controller__manufacturer',
                     'speed_controller__model', 'speed_controller__manufacturer', ]


class FlightControllerAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = FlightControllerSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = FlightController.objects.all().distinct()
    filterset_class = FlightControllerFilter
    search_fields = ['model', 'manufacturer', ]


class SpeedControllerAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = SpeedControllerSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = SpeedController.objects.all().distinct()
    filterset_class = SpeedControllerFilter
    search_fields = ['model', 'manufacturer', ]
