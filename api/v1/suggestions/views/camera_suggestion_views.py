from drf_rw_serializers.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.mixins import SuggestionActionsMixin
from api.v1.suggestions.serializers.camera_suggestion_serializers import VideoFormatSuggestionSerializer
from suggestions.models import VideoFormatSuggestion
from users.permissions import HasAcceptDeny


class VideoFormatSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = VideoFormatSuggestion
    serializer_class = VideoFormatSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return VideoFormatSuggestion.objects.distinct()
        else:
            return VideoFormatSuggestion.objects.filter(user=self.request.user).distinct()
