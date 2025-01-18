from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer
from api.v1.components.serializers.camera_serializers import VideoFormatSerializer
from api.v1.documents.serializers import TransmitterDocumentSerializer
from api.v1.galleries.serializers import TransmitterGallerySerializer
from components.models import OutputPower, Transmitter


class OutputPowerSerializers(serializers.ModelSerializer):

    class Meta:
        model = OutputPower
        fields = '__all__'


class TransmitterSerializer(serializers.ModelSerializer):
    output_powers = OutputPowerSerializers(many=True)
    video_formats = VideoFormatSerializer(many=True)
    antenna_connectors = AntennaConnectorSerializer(many=True)
    images = TransmitterGallerySerializer(many=True)
    documents = TransmitterDocumentSerializer(many=True)

    class Meta:
        model = Transmitter
        fields = '__all__'
