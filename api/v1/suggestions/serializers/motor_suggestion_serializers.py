from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from api.v1.components.serializers import MotorSerializer, MotorDetailSerializer, RatedVoltageSerializer
from api.v1.documents.serializers import MotorDocumentReadSerializer, MotorDocumentWriteSerializer
from api.v1.galleries.serializers import MotorGalleryReadSerializer, MotorGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from api.v1.users.serializers import UserSerializer
from components.models import Motor, RatedVoltage
from suggestions.models import (
    SuggestedMotorDetailSuggestion,
    MotorSuggestion,
    ExistingMotorDetailSuggestion,
    RatedVoltageSuggestion
)


class MotorDetailSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for motor details within suggestions"""
    voltage = serializers.PrimaryKeyRelatedField(
        queryset=RatedVoltage.objects.all(),
        required=True
    )

    class Meta:
        model = SuggestedMotorDetailSuggestion
        fields = ['weight', 'max_power', 'kv_per_volt', 'peak_current',
                 'idle_current', 'resistance', 'voltage']


class MotorSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    suggested_images = MotorGalleryWriteSerializer(many=True)
    suggested_documents = MotorDocumentWriteSerializer(many=True, required=False)
    suggested_details = MotorDetailSuggestionSerializer(many=True)
    related_instance = MotorSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = MotorSuggestion
        fields = '__all__'


class RatedVoltageSuggestionSerializer(BaseSuggestionSerializer):
    """Serializer for rated voltage suggestions"""
    related_instance = RatedVoltageSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = RatedVoltageSuggestion
        fields = '__all__'


class ExistingMotorDetailSuggestionSerializer(BaseSuggestionSerializer):
    """Serializer for existing motor detail suggestions"""
    motor = serializers.PrimaryKeyRelatedField(
        queryset=Motor.objects.all(),
        required=True
    )
    voltage = serializers.PrimaryKeyRelatedField(
        queryset=RatedVoltage.objects.all(),
        required=True
    )
    related_instance = MotorDetailSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = ExistingMotorDetailSuggestion
        fields = '__all__'