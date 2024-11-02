from rest_framework import serializers

from documents.models import (AntennaDocument, CameraDocument, DroneDocument, FrameDocument, MotorDocument, StackDocument,
                              PropellerDocument, ReceiverDocument, TransmitterDocument,
                              SpeedControllerDocument, FlightControllerDocument)


class AntennaDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaDocument
        fields = '__all__'


class CameraDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraDocument
        fields = '__all__'


class DroneDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneDocument
        fields = '__all__'


class FrameDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameDocument
        fields = '__all__'


class MotorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorDocument
        fields = '__all__'


class StackDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackDocument
        fields = '__all__'


class PropellerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropellerDocument
        fields = '__all__'


class ReceiverDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverDocument
        fields = '__all__'


class TransmitterDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmitterDocument
        fields = '__all__'


class SpeedControllerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedControllerDocument
        fields = '__all__'


class FlightControllerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightControllerDocument
        fields = '__all__'
