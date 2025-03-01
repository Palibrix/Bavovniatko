from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import AntennaTypeSerializer, AntennaSerializer, AntennaConnectorSerializer, \
    AntennaDetailSerializer
from api.v1.documents.serializers import AntennaDocumentWriteSerializer
from api.v1.galleries.serializers import AntennaGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from api.v1.users.serializers import UserSerializer
from components.models import AntennaConnector, AntennaType, Antenna
from suggestions.models import SuggestedAntennaDetailSuggestion, AntennaSuggestion, AntennaTypeSuggestion, \
    AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion


class AntennaDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for antenna details within suggestions"""
    connector_type = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        required=True
    )

    class Meta:
        model = SuggestedAntennaDetailSuggestion
        fields = ['connector_type', 'weight', 'angle_type']


class AntennaSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=AntennaType.objects.all(),
        required=True
    )
    suggested_images = AntennaGalleryWriteSerializer(many=True)
    suggested_documents = AntennaDocumentWriteSerializer(many=True, required=False)
    suggested_details = AntennaDetailSuggestionSerializer(many=True)
    related_instance = AntennaSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = AntennaSuggestion
        fields = '__all__'


class AntennaTypeSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = AntennaTypeSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = AntennaTypeSuggestion
        fields = '__all__'


class AntennaConnectorSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = AntennaConnectorSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = AntennaConnectorSuggestion
        fields = '__all__'


class ExistingAntennaDetailSuggestionSerializer(BaseSuggestionSerializer):
    antenna = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        required=True
    )
    connector_type = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        required=True
    )
    related_instance = AntennaDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingAntennaDetailSuggestion
        fields = '__all__'