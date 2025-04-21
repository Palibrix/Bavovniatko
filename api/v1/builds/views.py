from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.v1.builds.filters import DroneFilter
from api.v1.builds.serializers import DroneSerializer, DroneWriteSerializer
from builds.models import Drone


class DroneAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = DroneFilter
    search_fields = ['model', 'manufacturer']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DroneWriteSerializer
        return DroneSerializer

    def get_queryset(self):
        queryset = Drone.objects.all().distinct()

        if self.action == 'retrieve':
            return queryset

        user_id = self.request.user.id

        # Handle filtering by specific user_id for list views
        filter_user_id = self.request.query_params.get('user_id')
        if filter_user_id:
            return queryset.filter(user_id=filter_user_id)

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return queryset.filter(user_id=user_id)

        # Filter logic for list views
        show_user_drones = self.request.query_params.get('show_user_drones', 'false').lower() == 'true'

        if show_user_drones:
            if user_id:
                return queryset.filter(user_id=user_id)

        return queryset.filter(user__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
