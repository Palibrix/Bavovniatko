from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.motor_suggestion_serializers import (
    MotorSuggestionSerializer,
    ExistingMotorDetailSuggestionSerializer,
    RatedVoltageSuggestionSerializer
)
from suggestions.models import (
    MotorSuggestion,
    ExistingMotorDetailSuggestion,
    RatedVoltageSuggestion
)
from users.permissions import HasAcceptDeny


class MotorSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = MotorSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MotorSuggestion.objects.distinct()
        else:
            return MotorSuggestion.objects.filter(user=self.request.user).distinct()


class RatedVoltageSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = RatedVoltageSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return RatedVoltageSuggestion.objects.distinct()
        else:
            return RatedVoltageSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingMotorDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = ExistingMotorDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingMotorDetailSuggestion.objects.distinct()
        else:
            return ExistingMotorDetailSuggestion.objects.filter(user=self.request.user).distinct()