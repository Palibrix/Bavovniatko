from rest_framework import serializers

from api.v1.documents.serializers import CameraDocumentReadSerializer
from api.v1.galleries.serializers import CameraGalleryReadSerializer
from components.models import Camera, CameraDetail, VideoFormat


class VideoFormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFormat
        fields = '__all__'


class CameraDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CameraDetail
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    video_formats = VideoFormatSerializer(many=True)
    details = CameraDetailSerializer(many=True)
    images = CameraGalleryReadSerializer(many=True)
    documents = CameraDocumentReadSerializer(many=True)

    class Meta:
        model = Camera
        fields = '__all__'
