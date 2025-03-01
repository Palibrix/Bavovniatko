from rest_framework import status
from rest_framework.decorators import action
from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response


class SuggestionActionsMixin:

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        try:
            instance.accept()
            return Response({'message': 'Suggestion accepted'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        try:
            admin_comment = request.data.get('admin_comment')
            instance.deny(admin_comment=admin_comment)
            return Response({'message': 'Suggestion denied'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.status == 'approved':
            raise ValidationError("Cannot modify approved suggestion")

        # If denied suggestion is being modified, set it back to pending
        if instance.status == 'denied':
            serializer.save(status='pending')
        else:
            serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')
