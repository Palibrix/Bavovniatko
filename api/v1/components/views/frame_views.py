from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.components.filters import FrameFilter
from api.v1.components.mixins import BaseComponentFilterMixin
from api.v1.components.serializers import FrameSerializer
from components.models import Frame


class FrameAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet, BaseComponentFilterMixin):
    permission_classes = ()
    serializer_class = FrameSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Frame.objects.all().distinct()
    filterset_class = FrameFilter
    search_fields = ['model', 'manufacturer']
