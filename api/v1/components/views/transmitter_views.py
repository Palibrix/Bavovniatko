from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from api.v1.components.filters import TransmitterFilter
from api.v1.components.serializers import TransmitterSerializer
from components.models import Transmitter


class TransmitterAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = TransmitterSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Transmitter.objects.all().distinct()
    filterset_class = TransmitterFilter
    search_fields = ['model', 'manufacturer']
