from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import SuggestionActionsMixin
from rest_framework.viewsets import ModelViewSet

from api.v1.suggestions.serializers.antenna_suggestion_serializers import AntennaTypeSuggestionSerializer, \
    AntennaConnectorSuggestionSerializer, \
    ExistingAntennaDetailSuggestionSerializer, AntennaSuggestionSerializer
from components.models import AntennaType
from suggestions.models import AntennaSuggestion
# from drf_rw_serializers.viewsets import ModelViewSet

from suggestions.models.antenna_suggestions import AntennaTypeSuggestion, AntennaConnectorSuggestion, \
    ExistingAntennaDetailSuggestion
from users.permissions import HasAcceptDeny


class AntennaSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = AntennaSuggestion
    serializer_class = AntennaSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AntennaSuggestion.objects.distinct()
        else:
            return AntennaSuggestion.objects.filter(user=self.request.user).distinct()


class AntennaTypeSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = AntennaTypeSuggestion
    serializer_class = AntennaTypeSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AntennaTypeSuggestion.objects.distinct()
        else:
            return AntennaTypeSuggestion.objects.filter(user=self.request.user).distinct()


class AntennaConnectorSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = AntennaConnectorSuggestion
    serializer_class = AntennaConnectorSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AntennaConnectorSuggestion.objects.distinct()
        else:
            return AntennaConnectorSuggestion.objects.filter(user=self.request.user).distinct()


class ExistingAntennaDetailSuggestionAPIViewSet(SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = ExistingAntennaDetailSuggestion
    serializer_class = ExistingAntennaDetailSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExistingAntennaDetailSuggestion.objects.distinct()
        else:
            return ExistingAntennaDetailSuggestion.objects.filter(user=self.request.user).distinct()
