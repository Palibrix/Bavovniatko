from rest_framework import serializers

from api.v1.documents.serializers import CameraDocumentSerializer
from api.v1.galleries.serializers import CameraGallerySerializer
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
    video_formats = VideoFormatSerializers(many=True)
    details = CameraDetailSerializer(many=True)
    images = CameraGallerySerializer(many=True)
    documents = CameraDocumentSerializer(many=True)

    class Meta:
        model = Camera
        fields = '__all__'
