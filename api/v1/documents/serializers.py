
from rest_framework import serializers

from api.v1.documents.mixins import BaseDocumentWriteSerializer
from api.v1.utils import ReadOnlyModelSerializer
from components.models import Receiver
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


class StackDocumentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackDocument
        fields = '__all__'


class StackDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = StackDocument
        fields = ('id', 'file',)


class PropellerDocumentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropellerDocument
        fields = '__all__'


class PropellerDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = PropellerDocument
        fields = ('id', 'file',)


class ReceiverDocumentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverDocument
        fields = '__all__'


class ReceiverDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = ReceiverDocument
        fields = ('id', 'file',)


class TransmitterDocumentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmitterDocument
        fields = '__all__'


class TransmitterDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = TransmitterDocument
        fields = ('id', 'file',)


class SpeedControllerReadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedControllerDocument
        fields = '__all__'


class SpeedControllerDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = SpeedControllerDocument
        fields = ('id', 'file',)


class FlightControllerReadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightControllerDocument
        fields = '__all__'


class FlightControllerDocumentWriteSerializer(BaseDocumentWriteSerializer):
    class Meta:
        model = FlightControllerDocument
        fields = ('id', 'file',)
