from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.camera_suggestion_serializers import VideoFormatSuggestionSerializer, \
    CameraSuggestionSerializer, ExistingCameraDetailSuggestionSerializer
from suggestions.models import VideoFormatSuggestion, CameraSuggestion, ExistingCameraDetailSuggestion
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


class CameraSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = CameraSuggestion
    serializer_class = CameraSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CameraSuggestion.objects.distinct()
        else:
            return CameraSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingCameraDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingCameraDetailSuggestion
    serializer_class = ExistingCameraDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingCameraDetailSuggestion.objects.distinct()
        else:
            return ExistingCameraDetailSuggestion.objects.filter(user=self.request.user).distinct()