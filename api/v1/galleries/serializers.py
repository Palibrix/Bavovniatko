from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.v1.galleries.mixins import BaseGalleryWriteSerializer
from api.v1.utils import ReadOnlyModelSerializer
from galleries.models import (AntennaGallery, CameraGallery, DroneGallery, FrameGallery, MotorGallery, StackGallery,
                              PropellerGallery, ReceiverGallery, TransmitterGallery,
                              SpeedControllerGallery, FlightControllerGallery)


class AntennaGalleryReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = AntennaGallery
        fields = '__all__'


class AntennaGalleryWriteSerializer(BaseGalleryWriteSerializer):

    class Meta:
        model = AntennaGallery
        fields = ('id', 'image', 'order')


class CameraGalleryReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = CameraGallery
        fields = '__all__'


class CameraGalleryWriteSerializer(BaseGalleryWriteSerializer):

    class Meta:
        model = CameraGallery
        fields = ('id', 'image', 'order')


class DroneGalleryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneGallery
        fields = '__all__'


class DroneGalleryWriteSerializer(BaseGalleryWriteSerializer):
    class Meta:
        model = DroneGallery
        fields = ('id', 'image', 'order')


class FrameGalleryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameGallery
        fields = '__all__'


class FrameGalleryWriteSerializer(BaseGalleryWriteSerializer):
    class Meta:
        model = FrameGallery
        fields = ('id', 'image', 'order')


class MotorGalleryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorGallery
        fields = '__all__'


class MotorGalleryWriteSerializer(BaseGalleryWriteSerializer):
    class Meta:
        model = MotorGallery
        fields = ('id', 'image', 'order')


class StackGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StackGallery
        fields = '__all__'


class PropellerGalleryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropellerGallery
        fields = '__all__'


class PropellerGalleryWriteSerializer(BaseGalleryWriteSerializer):

    class Meta:
        model = PropellerGallery
        fields = ('id', 'image', 'order')


class ReceiverGalleryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverGallery
        fields = '__all__'


class ReceiverGalleryWriteSerializer(BaseGalleryWriteSerializer):

    class Meta:
        model = ReceiverGallery
        fields = ('id', 'image', 'order')


class TransmitterGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmitterGallery
        fields = '__all__'


class SpeedControllerGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedControllerGallery
        fields = '__all__'


class FlightControllerGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightControllerGallery
        fields = '__all__'
