from rest_framework import status
from rest_framework.decorators import action
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class SuggestionActionsMixin:

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