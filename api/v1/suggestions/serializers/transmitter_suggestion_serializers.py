from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import TransmitterSerializer, OutputPowerSerializer
from api.v1.documents.serializers import TransmitterDocumentWriteSerializer
from api.v1.galleries.serializers import TransmitterGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from components.models import VideoFormat, OutputPower, AntennaConnector
from suggestions.models import TransmitterSuggestion, OutputPowerSuggestion


class TransmitterSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    """Write serializer for transmitter suggestions with nested data handling"""
    video_formats = serializers.PrimaryKeyRelatedField(
        queryset=VideoFormat.objects.all(),
        many=True,
        required=False
    )
    output_powers = serializers.PrimaryKeyRelatedField(
        queryset=OutputPower.objects.all(),
        many=True,
        required=False
    )
    antenna_connectors = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        many=True,
        required=False
    )
    suggested_images = TransmitterGalleryWriteSerializer(many=True)
    suggested_documents = TransmitterDocumentWriteSerializer(many=True, required=False)
    related_instance = TransmitterSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = TransmitterSuggestion
        fields = '__all__'


class OutputPowerSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = OutputPowerSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = OutputPowerSuggestion
        fields = '__all__'