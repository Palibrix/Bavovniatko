from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet

from api.v1.suggestions.serializers.antenna_suggestion_serializers import AntennaSuggestionWriteSerializer, \
    AntennaSuggestionReadSerializer
from suggestions.models import AntennaSuggestion
from drf_rw_serializers.viewsets import ModelViewSet

from users.permissions import HasAcceptDeny


class AntennaSuggestionAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = AntennaSuggestion
    read_serializer_class = AntennaSuggestionReadSerializer
    write_serializer_class = AntennaSuggestionWriteSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AntennaSuggestion.objects.distinct()
        else:
            return AntennaSuggestion.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        suggestion = self.get_object()
        try:
            suggestion.accept()
            return Response({'message': 'Suggestion accepted'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        suggestion = self.get_object()
        try:
            admin_comment = request.data.get('admin_comment')
            suggestion.deny(admin_comment=admin_comment)
            return Response({'message': 'Suggestion denied'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))