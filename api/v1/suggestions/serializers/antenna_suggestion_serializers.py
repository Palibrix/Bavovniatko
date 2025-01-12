from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer, AntennaTypeSerializer, AntennaSerializer, \
    AntennaDetailSerializer
from api.v1.documents.serializers import AntennaDocumentReadSerializer, AntennaDocumentWriteSerializer
from api.v1.galleries.serializers import AntennaGalleryReadSerializer, AntennaGalleryWriteSerializer
from api.v1.suggestions.mixins import SuggestionUpdateMixin, ValidateSuggestionNestedFieldsMixin
from api.v1.users.serializers import UserSerializer
from api.v1.utils import ReadOnlyModelSerializer
from components.models import AntennaType, AntennaConnector, Antenna, AntennaDetail
from galleries.models import AntennaGallery
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_suggestions import SuggestedAntennaDetailSuggestion, AntennaTypeSuggestion, \
    AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion
from drf_writable_nested.serializers import WritableNestedModelSerializer

class SuggestedAntennaDetailSuggestionSerializer(serializers.ModelSerializer):
    connector_type = AntennaConnectorSerializer(read_only=True)
    connector_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        write_only=True,
        source='connector_type',
        many=False,
    )

    class Meta:
        model = SuggestedAntennaDetailSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'suggestion', 'connector_type', 'related_instance']


class AntennaSuggestionReadSerializer(ReadOnlyModelSerializer):
    type = AntennaTypeSerializer(read_only=True)
    suggested_images = AntennaGalleryReadSerializer(many=True, read_only=True)
    suggested_documents = AntennaDocumentReadSerializer(many=True, read_only=True)
    suggested_details = SuggestedAntennaDetailSuggestionSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AntennaSuggestion
        fields = '__all__'


class AntennaSuggestionWriteSerializer(SuggestionUpdateMixin, ValidateSuggestionNestedFieldsMixin, WritableNestedModelSerializer):
    type = AntennaTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaType.objects.all(),
        write_only=True,
        source='type',
    )
    related_instance = AntennaSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )
    suggested_images = AntennaGalleryWriteSerializer(many=True)
    suggested_documents = AntennaDocumentWriteSerializer(many=True, required=False)
    suggested_details = SuggestedAntennaDetailSuggestionSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AntennaSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'type', 'reviewed', 'accepted', 'admin_comment']


class AntennaTypeSuggestionSerializer(SuggestionUpdateMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_instance = AntennaTypeSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaType.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )

    class Meta:
        model = AntennaTypeSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'related_instance', 'reviewed', 'accepted', 'admin_comment']


class AntennaConnectorSuggestionSerializer(SuggestionUpdateMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_instance = AntennaConnectorSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )

    class Meta:
        model = AntennaConnectorSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'related_instance', 'reviewed', 'accepted', 'admin_comment']


class ExistingAntennaDetailSuggestionSerializer(SuggestionUpdateMixin, serializers.ModelSerializer):
    antenna = AntennaSerializer(read_only=True)
    antenna_id = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        write_only=True,
        source='antenna'
    )

    related_instance = AntennaDetailSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaDetail.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )

    connector_type = AntennaConnectorSerializer(read_only=True)
    connector_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        write_only=True,
        source='connector_type',
        many=False,
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = ExistingAntennaDetailSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'reviewed', 'accepted', 'admin_comment']