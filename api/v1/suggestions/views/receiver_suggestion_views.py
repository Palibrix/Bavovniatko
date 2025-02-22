from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.camera_suggestion_serializers import VideoFormatSuggestionSerializer, \
    CameraSuggestionSerializer, ExistingCameraDetailSuggestionSerializer
from api.v1.suggestions.serializers.receiver_suggestion_serializers import ReceiverProtocolTypeSuggestionSerializer, \
    ReceiverSuggestionSerializer, ExistingReceiverDetailSuggestionSerializer
from suggestions.models import VideoFormatSuggestion, CameraSuggestion, ExistingCameraDetailSuggestion, \
    ReceiverProtocolTypeSuggestion, ReceiverSuggestion, ExistingReceiverDetailSuggestion
from users.permissions import HasAcceptDeny


class ReceiverProtocolTypeSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ReceiverProtocolTypeSuggestion
    serializer_class = ReceiverProtocolTypeSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ReceiverProtocolTypeSuggestion.objects.distinct()
        else:
            return ReceiverProtocolTypeSuggestion.objects.filter(user=self.request.user).distinct()


class ReceiverSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ReceiverSuggestion
    serializer_class = ReceiverSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ReceiverSuggestion.objects.distinct()
        else:
            return ReceiverSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingReceiverDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingReceiverDetailSuggestion
    serializer_class = ExistingReceiverDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingReceiverDetailSuggestion.objects.distinct()
        else:
            return ExistingReceiverDetailSuggestion.objects.filter(user=self.request.user).distinct()