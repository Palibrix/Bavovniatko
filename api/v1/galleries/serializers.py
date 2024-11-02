from rest_framework import serializers

from galleries.models import (AntennaGallery, CameraGallery, DroneGallery, FrameGallery, MotorGallery, StackGallery,
                              PropellerGallery, ReceiverGallery, TransmitterGallery,
                              SpeedControllerGallery, FlightControllerGallery)


class AntennaGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaGallery
        fields = '__all__'


class CameraGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraGallery
        fields = '__all__'


class DroneGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneGallery
        fields = '__all__'


class FrameGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameGallery
        fields = '__all__'


class MotorGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorGallery
        fields = '__all__'


class StackGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StackGallery
        fields = '__all__'


class PropellerGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropellerGallery
        fields = '__all__'


class ReceiverGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverGallery
        fields = '__all__'


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
