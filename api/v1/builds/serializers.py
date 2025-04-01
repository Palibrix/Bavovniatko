from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import (AntennaSerializer, CameraSerializer, FrameSerializer, \
                                           MotorSerializer, PropellerSerializer, ReceiverSerializer,
                                           TransmitterSerializer,
                                           SpeedControllerSerializer, FlightControllerSerializer)
from api.v1.components.serializers.battery_serializers import BatterySerializer
from api.v1.documents.serializers import DroneDocumentReadSerializer, DroneDocumentWriteSerializer
from api.v1.galleries.serializers import DroneGalleryReadSerializer, DroneGalleryWriteSerializer
from api.v1.users.serializers import UserSerializer
from builds.models import Drone
from components.models import Antenna, Camera, Battery, Frame, FlightController, Motor, Propeller, Receiver, \
    SpeedController, Transmitter


class DroneSerializer(serializers.ModelSerializer):
    antenna_receiver = AntennaSerializer(read_only=True)
    antenna_transmitter = AntennaSerializer(read_only=True)
    camera = CameraSerializer(read_only=True)
    battery = BatterySerializer(read_only=True)
    frame = FrameSerializer(read_only=True)
    flight_controller = FlightControllerSerializer(read_only=True)
    motor = MotorSerializer(read_only=True)
    propeller = PropellerSerializer(read_only=True)
    receiver = ReceiverSerializer(read_only=True)
    speed_controller = SpeedControllerSerializer(read_only=True)
    transmitter = TransmitterSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    images = DroneGalleryReadSerializer(many=True)
    documents = DroneDocumentReadSerializer(many=True)

    class Meta:
        model = Drone
        fields = '__all__'


class DroneWriteSerializer(WritableNestedModelSerializer):
    """Write serializer for creating and updating drones"""
    images = DroneGalleryWriteSerializer(many=True, required=False)
    documents = DroneDocumentWriteSerializer(many=True, required=False)

    # Component relationships
    antenna_receiver = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        required=False, allow_null=True
    )
    antenna_transmitter = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        required=False, allow_null=True
    )
    camera = serializers.PrimaryKeyRelatedField(
        queryset=Camera.objects.all(),
        required=False, allow_null=True
    )
    battery = serializers.PrimaryKeyRelatedField(
        queryset=Battery.objects.all(),
        required=False, allow_null=True
    )
    frame = serializers.PrimaryKeyRelatedField(
        queryset=Frame.objects.all(),
        required=False, allow_null=True
    )
    flight_controller = serializers.PrimaryKeyRelatedField(
        queryset=FlightController.objects.all(),
        required=False, allow_null=True
    )
    motor = serializers.PrimaryKeyRelatedField(
        queryset=Motor.objects.all(),
        required=False, allow_null=True
    )
    propeller = serializers.PrimaryKeyRelatedField(
        queryset=Propeller.objects.all(),
        required=False, allow_null=True
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=Receiver.objects.all(),
        required=False, allow_null=True
    )
    speed_controller = serializers.PrimaryKeyRelatedField(
        queryset=SpeedController.objects.all(),
        required=False, allow_null=True
    )
    transmitter = serializers.PrimaryKeyRelatedField(
        queryset=Transmitter.objects.all(),
        required=False, allow_null=True
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Drone
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
