from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer
from api.v1.components.serializers.camera_serializers import VideoFormatSerializer
from api.v1.documents.serializers import TransmitterDocumentReadSerializer
from api.v1.galleries.serializers import TransmitterGalleryReadSerializer
from components.models import OutputPower, Transmitter


class OutputPowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutputPower
        fields = '__all__'


class TransmitterSerializer(serializers.ModelSerializer):
    output_powers = OutputPowerSerializer(many=True)
    video_formats = VideoFormatSerializer(many=True)
    antenna_connectors = AntennaConnectorSerializer(many=True)
    images = TransmitterGalleryReadSerializer(many=True)
    documents = TransmitterDocumentReadSerializer(many=True)

    class Meta:
        model = Transmitter
        fields = '__all__'
