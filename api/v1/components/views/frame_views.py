from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.components.serializers import FrameSerializer
from components.models import Frame


class FrameAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = FrameSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Frame.objects.all().distinct()
    filterset_fields = ['manufacturer', 'prop_size', 'material', 'configuration',
                        'camera_details__camera_mount_height', 'camera_details__camera_mount_width',
                        'motor_details__motor_mount_height', 'motor_details__motor_mount_width',
                        'vtx_details__vtx_mount_height', 'vtx_details__vtx_mount_width',]
    search_fields = ['model', 'manufacturer']
