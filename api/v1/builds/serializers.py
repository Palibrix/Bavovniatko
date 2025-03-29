from rest_framework import serializers

from api.v1.components.serializers import (AntennaSerializer, CameraSerializer, FrameSerializer, \
    MotorSerializer, PropellerSerializer, ReceiverSerializer, TransmitterSerializer,
                                           SpeedControllerSerializer, FlightControllerSerializer)
from api.v1.components.serializers.battery_serializers import BatterySerializer
from api.v1.documents.serializers import DroneDocumentReadSerializer
from api.v1.galleries.serializers import DroneGalleryReadSerializer
from builds.models import Drone


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

    images = DroneGalleryReadSerializer(many=True)
    documents = DroneDocumentReadSerializer(many=True)

    class Meta:
        model = Drone
        fields = '__all__'
