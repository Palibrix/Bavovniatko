from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.v1.utils import ReadOnlyModelSerializer
from galleries.models import (AntennaGallery, CameraGallery, DroneGallery, FrameGallery, MotorGallery, StackGallery,
                              PropellerGallery, ReceiverGallery, TransmitterGallery,
                              SpeedControllerGallery, FlightControllerGallery)


class AntennaGalleryReadSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = AntennaGallery
        fields = '__all__'


class AntennaGalleryWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaGallery.objects.values_list('id', flat=True),
        write_only=True,
        many=False,
        required=False,
    )
    image = Base64ImageField()

    class Meta:
        model = AntennaGallery
        fields = ('id', 'image', 'order')
        # read_only_fields = ('object', 'suggestion', 'accepted')


class CameraGallerySerializer(ReadOnlyModelSerializer):
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
