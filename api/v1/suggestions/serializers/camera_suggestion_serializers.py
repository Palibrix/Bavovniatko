from rest_framework import serializers

from api.v1.components.serializers.camera_serializers import VideoFormatSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from api.v1.users.serializers import UserSerializer
from components.models import VideoFormat
from suggestions.models import VideoFormatSuggestion


class VideoFormatSuggestionSerializer(BaseSuggestionSerializer):
    user = UserSerializer(read_only=True)
    related_instance = VideoFormatSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = VideoFormatSuggestion
        fields = '__all__'