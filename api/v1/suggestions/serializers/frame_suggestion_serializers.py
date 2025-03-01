from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import FrameSerializer, FrameCameraDetailSerializer, FrameMotorDetailSerializer, \
    FrameVTXDetailSerializer
from api.v1.documents.serializers import FrameDocumentWriteSerializer
from api.v1.galleries.serializers import FrameGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from components.models import Frame
from suggestions.models import SuggestedFrameCameraDetailSuggestion, FrameSuggestion, \
    SuggestedFrameMotorDetailSuggestion, SuggestedFrameVTXDetailSuggestion, \
    ExistingFrameCameraDetailSuggestion, ExistingFrameMotorDetailSuggestion, ExistingFrameVTXDetailSuggestion


class FrameCameraDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for frame camera details within suggestions"""
    class Meta:
        model = SuggestedFrameCameraDetailSuggestion
        fields = ['camera_mount_height', 'camera_mount_width']


class FrameMotorDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for frame motor details within suggestions"""
    class Meta:
        model = SuggestedFrameMotorDetailSuggestion
        fields = ['motor_mount_height', 'motor_mount_width']


class FrameVTXDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for frame VTX details within suggestions"""
    class Meta:
        model = SuggestedFrameVTXDetailSuggestion
        fields = ['vtx_mount_height', 'vtx_mount_width']


class FrameSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    """Write serializer for frame suggestions with nested data handling"""
    suggested_camera_details = FrameCameraDetailSuggestionSerializer(many=True)
    suggested_motor_details = FrameMotorDetailSuggestionSerializer(many=True)
    suggested_vtx_details = FrameVTXDetailSuggestionSerializer(many=True)
    suggested_images = FrameGalleryWriteSerializer(many=True)
    suggested_documents = FrameDocumentWriteSerializer(many=True, required=False)
    related_instance = FrameSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = FrameSuggestion
        fields = '__all__'


class ExistingFrameCameraDetailSuggestionSerializer(BaseSuggestionSerializer):
    frame = serializers.PrimaryKeyRelatedField(
        queryset=Frame.objects.all(),
        required=True
    )
    related_instance = FrameCameraDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingFrameCameraDetailSuggestion
        fields = '__all__'


class ExistingFrameMotorDetailSuggestionSerializer(BaseSuggestionSerializer):
    frame = serializers.PrimaryKeyRelatedField(
        queryset=Frame.objects.all(),
        required=True
    )
    related_instance = FrameMotorDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingFrameMotorDetailSuggestion
        fields = '__all__'


class ExistingFrameVTXDetailSuggestionSerializer(BaseSuggestionSerializer):
    frame = serializers.PrimaryKeyRelatedField(
        queryset=Frame.objects.all(),
        required=True
    )
    related_instance = FrameVTXDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingFrameVTXDetailSuggestion
        fields = '__all__'