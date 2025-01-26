
from rest_framework import serializers

from api.v1.documents.mixins import BaseDocumentWriteSerializer
from api.v1.utils import ReadOnlyModelSerializer
from documents.models import (AntennaDocument, CameraDocument, DroneDocument, FrameDocument, MotorDocument,
                              StackDocument,
                              PropellerDocument, ReceiverDocument, TransmitterDocument,
                              SpeedControllerDocument, FlightControllerDocument)


class AntennaDocumentReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = AntennaDocument
        fields = '__all__'


class AntennaDocumentWriteSerializer(BaseDocumentWriteSerializer):

    class Meta:
        model = AntennaDocument
        fields = ('id', 'file',)


class CameraDocumentReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = CameraDocument
        fields = '__all__'


class CameraDocumentWriteSerializer(BaseDocumentWriteSerializer):

    class Meta:
        model = CameraDocument
        fields = ('id', 'file',)


class DroneDocumentReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DroneDocument
        fields = '__all__'


class DroneDocumentWriteSerializer(BaseDocumentWriteSerializer):

    class Meta:
        model = CameraDocument
        fields = ('id', 'file',)


class FrameDocumentReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = FrameDocument
        fields = '__all__'


class FrameDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = FrameDocument
        fields = ('id', 'file',)


class MotorDocumentReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = MotorDocument
        fields = '__all__'


class MotorDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = MotorDocument
        fields = ('id', 'file',)


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
