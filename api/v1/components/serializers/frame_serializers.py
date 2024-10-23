from rest_framework import serializers

from components.models import FrameCameraDetail, FrameMotorDetail, FrameVTXDetail, Frame


class FrameCameraDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrameCameraDetail
        fields = '__all__'


class FrameMotorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrameMotorDetail
        fields = '__all__'


class FrameVTXDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrameVTXDetail
        fields = '__all__'


class FrameSerializer(serializers.ModelSerializer):
    camera_details = FrameCameraDetailSerializer(many=True, read_only=True)
    motor_details = FrameMotorDetailSerializer(many=True, read_only=True)
    vtx_details = FrameVTXDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Frame
        fields = '__all__'