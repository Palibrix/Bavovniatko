from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.transmitter_suggestion_serializers import (
    TransmitterSuggestionSerializer,
    OutputPowerSuggestionSerializer
)
from suggestions.models import TransmitterSuggestion, OutputPowerSuggestion
from users.permissions import HasAcceptDeny


class TransmitterSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = TransmitterSuggestion
    serializer_class = TransmitterSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return TransmitterSuggestion.objects.distinct()
        else:
            return TransmitterSuggestion.objects.filter(user=self.request.user).distinct()


class OutputPowerSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = OutputPowerSuggestion
    serializer_class = OutputPowerSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return OutputPowerSuggestion.objects.distinct()
        else:
            return OutputPowerSuggestion.objects.filter(user=self.request.user).distinct()