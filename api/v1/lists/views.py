from rest_framework.viewsets import ModelViewSet

from api.v1.lists.serializers import ListSerializer
from lists.models import List


class ListAPIViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    model = List

    def get_queryset(self):
        return List.objects.filter(owner=self.request.user).distinct()