from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.components.filters import CameraFilter
from api.v1.components.serializers import CameraSerializer
from components.models import Camera


class CameraAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = CameraSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Camera.objects.all().distinct()
    filterset_class = CameraFilter
    search_fields = ['model', 'manufacturer']
