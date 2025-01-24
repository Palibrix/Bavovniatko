from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers.camera_serializers import VideoFormatSerializer, CameraSerializer, \
    CameraDetailSerializer
from api.v1.documents.serializers import CameraDocumentWriteSerializer
from api.v1.galleries.serializers import CameraGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from api.v1.users.serializers import UserSerializer
from components.models import VideoFormat, Camera
from suggestions.models import VideoFormatSuggestion, SuggestedCameraDetailSuggestion, CameraSuggestion, \
    ExistingCameraDetailSuggestion


class VideoFormatSuggestionSerializer(BaseSuggestionSerializer):
    user = UserSerializer(read_only=True)
    related_instance = VideoFormatSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = VideoFormatSuggestion
        fields = '__all__'


class CameraDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for camera details within suggestions"""
    class Meta:
        model = SuggestedCameraDetailSuggestion
        fields = ['height', 'width']


class CameraSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    """Write serializer for camera suggestions with nested data handling"""
    video_formats = serializers.PrimaryKeyRelatedField(
        queryset=VideoFormat.objects.all(),
        many=True,
        required=True
    )
    suggested_images = CameraGalleryWriteSerializer(many=True)
    suggested_documents = CameraDocumentWriteSerializer(many=True, required=False)
    suggested_details = CameraDetailSuggestionSerializer(many=True)
    related_instance = CameraSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = CameraSuggestion
        fields = '__all__'


class ExistingCameraDetailSuggestionSerializer(BaseSuggestionSerializer):
    camera = serializers.PrimaryKeyRelatedField(
        queryset=Camera.objects.all(),
        required=True
    )
    related_instance = CameraDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingCameraDetailSuggestion
        fields = '__all__'