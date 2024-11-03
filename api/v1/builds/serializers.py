from rest_framework import serializers

from api.v1.components.serializers import (AntennaSerializer, CameraSerializer, FrameSerializer, \
    MotorSerializer, PropellerSerializer, ReceiverSerializer, TransmitterSerializer,
                                           SpeedControllerSerializer, FlightControllerSerializer)
from builds.models import Drone


class DroneSerializer(serializers.ModelSerializer):
    antenna = AntennaSerializer(read_only=True)
    camera = CameraSerializer(read_only=True)
    frame = FrameSerializer(read_only=True)
    flight_controller = FlightControllerSerializer(read_only=True)
    motor = MotorSerializer(read_only=True)
    propeller = PropellerSerializer(read_only=True)
    receiver = ReceiverSerializer(read_only=True)
    speed_controller = SpeedControllerSerializer(read_only=True)
    transmitter = TransmitterSerializer(read_only=True)

    class Meta:
        model = Drone
        fields = '__all__'
