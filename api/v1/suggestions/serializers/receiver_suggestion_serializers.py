from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import ReceiverSerializer, ReceiverProtocolTypeSerializer, ReceiverDetailSerializer
from api.v1.documents.serializers import ReceiverDocumentWriteSerializer
from api.v1.galleries.serializers import ReceiverGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from components.models import AntennaConnector, ReceiverProtocolType, Receiver
from suggestions.models import ReceiverSuggestion, SuggestedReceiverDetailSuggestion, ExistingReceiverDetailSuggestion, \
    ReceiverProtocolTypeSuggestion


class ReceiverDetailSuggestionSerializer(BaseSuggestionSerializer):
    """Serializer for details within suggestions"""
    class Meta:
        model = SuggestedReceiverDetailSuggestion
        fields = ('frequency', 'weight', 'telemetry_power', 'rf_chip')


class ReceiverSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    antenna_connectors = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        many=True,
        required=False,
    )
    protocols = serializers.PrimaryKeyRelatedField(
        queryset=ReceiverProtocolType.objects.all(),
        many=True,
        required=False,
    )

    suggested_images = ReceiverGalleryWriteSerializer(many=True)
    suggested_documents = ReceiverDocumentWriteSerializer(many=True, required=False)
    suggested_details = ReceiverDetailSuggestionSerializer(many=True)
    related_instance = ReceiverSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ReceiverSuggestion
        fields = '__all__'


class ReceiverProtocolTypeSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = ReceiverProtocolTypeSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ReceiverProtocolTypeSuggestion
        fields = '__all__'


class ExistingReceiverDetailSuggestionSerializer(BaseSuggestionSerializer):
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=Receiver.objects.all(),
        required=True
    )
    related_instance = ReceiverDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingReceiverDetailSuggestion
        fields = '__all__'
