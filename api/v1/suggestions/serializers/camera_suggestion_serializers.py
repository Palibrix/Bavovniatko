from rest_framework import serializers

from api.v1.components.serializers.camera_serializers import VideoFormatSerializer
from api.v1.suggestions.mixins import SuggestionUpdateMixin
from api.v1.users.serializers import UserSerializer
from components.models import VideoFormat
from suggestions.models import VideoFormatSuggestion


class VideoFormatSuggestionSerializer(SuggestionUpdateMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_instance = VideoFormatSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=VideoFormat.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )

    class Meta:
        model = VideoFormatSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'related_instance', 'reviewed', 'accepted', 'admin_comment']