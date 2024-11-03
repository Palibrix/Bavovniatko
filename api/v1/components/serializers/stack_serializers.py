from rest_framework import serializers

from api.v1.components.serializers import RatedVoltageSerializer
from api.v1.documents.serializers import StackDocumentSerializer, FlightControllerDocumentSerializer, \
    SpeedControllerDocumentSerializer
from api.v1.galleries.serializers import StackGallerySerializer, FlightControllerGallerySerializer, \
    SpeedControllerGallerySerializer
from components.models import (Stack,
                               SpeedController, SpeedControllerProtocol, SpeedControllerFirmware,
                               FlightController, FlightControllerFirmware, Gyro)


class GyroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gyro
        fields = '__all__'


class FlightControllerFirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightControllerFirmware
        fields = '__all__'


class SpeedControllerFirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedControllerFirmware
        fields = '__all__'


class SpeedControllerProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedControllerProtocol
        fields = '__all__'


class FlightControllerSerializer(serializers.ModelSerializer):
    gyro = GyroSerializer(read_only=True)
    voltage = RatedVoltageSerializer(read_only=True)
    firmwares = FlightControllerFirmwareSerializer(many=True, read_only=True)
    stacks = serializers.SerializerMethodField()

    images = FlightControllerGallerySerializer(many=True)
    documents = FlightControllerDocumentSerializer(many=True)

    def get_stacks(self, obj):
        stacks = obj.stack_set.all()
        return StackSerializer(stacks, many=True).data

    class Meta:
        model = FlightController
        fields = '__all__'


class SingleFlightControllerSerializer(serializers.ModelSerializer):
    gyro = GyroSerializer(read_only=True)
    voltage = RatedVoltageSerializer(read_only=True)
    firmwares = FlightControllerFirmwareSerializer(many=True, read_only=True)

    images = FlightControllerGallerySerializer(many=True)
    documents = FlightControllerDocumentSerializer(many=True)

    class Meta:
        model = FlightController
        fields = '__all__'


class SpeedControllerSerializer(serializers.ModelSerializer):
    firmwares = SpeedControllerFirmwareSerializer(many=True, read_only=True)
    protocols = SpeedControllerProtocolSerializer(many=True, read_only=True)
    voltage = RatedVoltageSerializer(read_only=True)
    stacks = serializers.SerializerMethodField()

    images = SpeedControllerGallerySerializer(many=True)
    documents = SpeedControllerDocumentSerializer(many=True)

    def get_stacks(self, obj):
        stacks = obj.stack_set.all()
        return StackSerializer(stacks, many=True).data

    class Meta:
        model = SpeedController
        fields = '__all__'


class SingleSpeedControllerSerializer(serializers.ModelSerializer):
    firmwares = SpeedControllerFirmwareSerializer(many=True, read_only=True)
    protocols = SpeedControllerProtocolSerializer(many=True, read_only=True)
    voltage = RatedVoltageSerializer(read_only=True)
    images = SpeedControllerGallerySerializer(many=True)
    documents = SpeedControllerDocumentSerializer(many=True)

    class Meta:
        model = SpeedController
        fields = '__all__'


class StackSerializer(serializers.ModelSerializer):
    flight_controller = SingleFlightControllerSerializer(read_only=True)
    speed_controller = SingleSpeedControllerSerializer(read_only=True)
    images = StackGallerySerializer(many=True)
    documents = StackDocumentSerializer(many=True)

    class Meta:
        model = Stack
        fields = '__all__'
