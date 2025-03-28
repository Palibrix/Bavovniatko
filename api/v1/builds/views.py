from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.v1.builds.filters import DroneFilter
from api.v1.builds.serializers import DroneSerializer
from builds.models import Drone


class DroneAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = DroneSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = DroneFilter
    search_fields = ['model', 'manufacturer']

    def get_queryset(self):
        queryset = Drone.objects.all().distinct()

        # For detail view, don't filter the queryset
        if self.action == 'retrieve':
            return queryset

        # Filter logic for list views
        user_id = self.request.query_params.get('user_id')
        include_user_drones = self.request.query_params.get('include_user_drones', 'false').lower() == 'true'

        if user_id:
            # Get drones for a specific user
            queryset = queryset.filter(user_id=user_id)
        elif not include_user_drones:
            # By default, show only official drones
            queryset = queryset.filter(user__isnull=True)

        return queryset