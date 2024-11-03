from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from api.v1.components.filters import ReceiverFilter
from api.v1.components.serializers import ReceiverSerializer
from components.models import Receiver


class ReceiverAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = ReceiverSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Receiver.objects.all().distinct()
    filterset_class = ReceiverFilter
    search_fields = ['model', 'manufacturer', 'processor', 'details__rf_chip']
