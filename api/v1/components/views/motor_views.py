from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.components.filters import MotorFilter
from api.v1.components.serializers import MotorSerializer
from components.models import Motor


class MotorAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = MotorSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Motor.objects.all().distinct()
    filterset_class = MotorFilter
    search_fields = ['model', 'manufacturer']
