from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.v1.components.serializers import MotorSerializer
from components.models import Motor


class MotorAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = MotorSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    queryset = Motor.objects.all().distinct()
    filterset_fields = ['manufacturer', 'stator_diameter', 'stator_height',

                        'details__max_power', 'details__kv_per_volt',
                        'details__peak_current', 'details__idle_current',

                        'details__voltage__min_cells', 'details__voltage__max_cells',
                        'details__voltage__type'
                        ]
    search_fields = ['model', 'manufacturer']
