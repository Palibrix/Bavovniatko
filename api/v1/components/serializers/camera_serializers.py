from rest_framework import serializers

from components.models import Camera, CameraDetail, VideoFormat


class VideoFormatSerializers(serializers.ModelSerializer):

    class Meta:
        model = VideoFormat
        fields = '__all__'


class CameraDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CameraDetail
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    video_formats = VideoFormatSerializers(many=True, read_only=True)
    details = CameraDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'