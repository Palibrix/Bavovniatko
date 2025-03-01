from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.stack_suggestion_serializers import (
    FlightControllerSuggestionSerializer,
    SpeedControllerSuggestionSerializer,
    StackSuggestionSerializer,
    GyroSuggestionSerializer,
    FlightControllerFirmwareSuggestionSerializer,
    SpeedControllerFirmwareSuggestionSerializer,
    SpeedControllerProtocolSuggestionSerializer
)
from suggestions.models import (
    FlightControllerSuggestion,
    SpeedControllerSuggestion,
    StackSuggestion,
    GyroSuggestion,
    FlightControllerFirmwareSuggestion,
    SpeedControllerFirmwareSuggestion,
    SpeedControllerProtocolSuggestion
)
from users.permissions import HasAcceptDeny


class FlightControllerSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = FlightControllerSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlightControllerSuggestion.objects.distinct()
        return FlightControllerSuggestion.objects.filter(user=self.request.user).distinct()


class SpeedControllerSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = SpeedControllerSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SpeedControllerSuggestion.objects.distinct()
        return SpeedControllerSuggestion.objects.filter(user=self.request.user).distinct()


class StackSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = StackSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return StackSuggestion.objects.distinct()
        return StackSuggestion.objects.filter(user=self.request.user).distinct()


class GyroSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = GyroSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GyroSuggestion.objects.distinct()
        return GyroSuggestion.objects.filter(user=self.request.user).distinct()


class FlightControllerFirmwareSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = FlightControllerFirmwareSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlightControllerFirmwareSuggestion.objects.distinct()
        return FlightControllerFirmwareSuggestion.objects.filter(user=self.request.user).distinct()


class SpeedControllerFirmwareSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = SpeedControllerFirmwareSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SpeedControllerFirmwareSuggestion.objects.distinct()
        return SpeedControllerFirmwareSuggestion.objects.filter(user=self.request.user).distinct()


class SpeedControllerProtocolSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    serializer_class = SpeedControllerProtocolSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SpeedControllerProtocolSuggestion.objects.distinct()
        return SpeedControllerProtocolSuggestion.objects.filter(user=self.request.user).distinct()