from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.frame_suggestion_serializers import (
    FrameSuggestionSerializer,
    ExistingFrameCameraDetailSuggestionSerializer,
    ExistingFrameMotorDetailSuggestionSerializer,
    ExistingFrameVTXDetailSuggestionSerializer
)
from suggestions.models import (
    FrameSuggestion,
    ExistingFrameCameraDetailSuggestion,
    ExistingFrameMotorDetailSuggestion,
    ExistingFrameVTXDetailSuggestion
)
from users.permissions import HasAcceptDeny


class FrameSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = FrameSuggestion
    serializer_class = FrameSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FrameSuggestion.objects.distinct()
        else:
            return FrameSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingFrameCameraDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingFrameCameraDetailSuggestion
    serializer_class = ExistingFrameCameraDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingFrameCameraDetailSuggestion.objects.distinct()
        else:
            return ExistingFrameCameraDetailSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingFrameMotorDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingFrameMotorDetailSuggestion
    serializer_class = ExistingFrameMotorDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingFrameMotorDetailSuggestion.objects.distinct()
        else:
            return ExistingFrameMotorDetailSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingFrameVTXDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingFrameVTXDetailSuggestion
    serializer_class = ExistingFrameVTXDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingFrameVTXDetailSuggestion.objects.distinct()
        else:
            return ExistingFrameVTXDetailSuggestion.objects.filter(user=self.request.user).distinct()