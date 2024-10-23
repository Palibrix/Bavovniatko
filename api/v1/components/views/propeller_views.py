from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.components.serializers import PropellerSerializer
from components.models import Propeller


class PropellerAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = PropellerSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Propeller.objects.all().distinct()
    filterset_fields = ['manufacturer', 'blade_count']
    search_fields = ['model', 'manufacturer']
