from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.components.serializers import CameraSerializer
from components.models import Camera


class CameraAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = CameraSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Camera.objects.all().distinct()
    filterset_fields = ['manufacturer', 'voltage_min', 'voltage_max',
                        'ratio', 'output_type', 'video_formats__format', 'light_sens']
    search_fields = ['model', 'manufacturer']
