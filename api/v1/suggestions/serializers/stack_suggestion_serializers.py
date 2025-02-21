from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import (
    FlightControllerSerializer, SpeedControllerSerializer,
    StackSerializer, GyroSerializer,
    FlightControllerFirmwareSerializer,
    SpeedControllerFirmwareSerializer,
    SpeedControllerProtocolSerializer
)
from api.v1.documents.serializers import (
    FlightControllerDocumentWriteSerializer,
    SpeedControllerDocumentWriteSerializer,
    StackDocumentWriteSerializer
)
from api.v1.galleries.serializers import (
    FlightControllerGalleryWriteSerializer,
    SpeedControllerGalleryWriteSerializer,
    StackGalleryWriteSerializer
)
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from components.models import (
    Gyro, FlightControllerFirmware,
    SpeedControllerFirmware, SpeedControllerProtocol, FlightController, SpeedController, RatedVoltage
)
from suggestions.models import (
    FlightControllerSuggestion, SpeedControllerSuggestion,
    StackSuggestion, GyroSuggestion,
    FlightControllerFirmwareSuggestion,
    SpeedControllerFirmwareSuggestion,
    SpeedControllerProtocolSuggestion
)


class FlightControllerSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    firmwares = serializers.PrimaryKeyRelatedField(
        queryset=FlightControllerFirmware.objects.all(),
        many=True,
        required=False
    )
    gyro = serializers.PrimaryKeyRelatedField(
        queryset=Gyro.objects.all(),
    )
    voltage = serializers.PrimaryKeyRelatedField(
        queryset=RatedVoltage.objects.all(),
    )
    suggested_images = FlightControllerGalleryWriteSerializer(many=True)
    suggested_documents = FlightControllerDocumentWriteSerializer(many=True, required=False)
    related_instance = FlightControllerSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = FlightControllerSuggestion
        fields = '__all__'


class SpeedControllerSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    firmwares = serializers.PrimaryKeyRelatedField(
        queryset=SpeedControllerFirmware.objects.all(),
        many=True,
        required=False
    )
    protocols = serializers.PrimaryKeyRelatedField(
        queryset=SpeedControllerProtocol.objects.all(),
        many=True,
        required=False
    )
    voltage = serializers.PrimaryKeyRelatedField(
        queryset=RatedVoltage.objects.all(),
    )
    suggested_images = SpeedControllerGalleryWriteSerializer(many=True)
    suggested_documents = SpeedControllerDocumentWriteSerializer(many=True, required=False)
    related_instance = SpeedControllerSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = SpeedControllerSuggestion
        fields = '__all__'


class StackSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    flight_controller = serializers.PrimaryKeyRelatedField(
        queryset=FlightController.objects.all(),
        required=True
    )
    speed_controller = serializers.PrimaryKeyRelatedField(
        queryset=SpeedController.objects.all(),
        required=True
    )
    suggested_images = StackGalleryWriteSerializer(many=True)
    suggested_documents = StackDocumentWriteSerializer(many=True, required=False)
    related_instance = StackSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = StackSuggestion
        fields = '__all__'


class GyroSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = GyroSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = GyroSuggestion
        fields = '__all__'


class FlightControllerFirmwareSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = FlightControllerFirmwareSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = FlightControllerFirmwareSuggestion
        fields = '__all__'


class SpeedControllerFirmwareSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = SpeedControllerFirmwareSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = SpeedControllerFirmwareSuggestion
        fields = '__all__'


class SpeedControllerProtocolSuggestionSerializer(BaseSuggestionSerializer):
    related_instance = SpeedControllerProtocolSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = SpeedControllerProtocolSuggestion
        fields = '__all__'