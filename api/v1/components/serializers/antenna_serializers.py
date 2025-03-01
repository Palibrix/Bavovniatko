from rest_framework import serializers

from api.v1.documents.serializers import AntennaDocumentReadSerializer
from api.v1.galleries.serializers import AntennaGalleryReadSerializer
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector


class AntennaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaType
        fields = ('type', 'direction', 'polarization')


class AntennaConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaConnector
        fields = ('type',)


class AntennaDetailSerializer(serializers.ModelSerializer):
    connector_type = AntennaConnectorSerializer(read_only=True)

    class Meta:
        model = AntennaDetail
        fields = '__all__'


class AntennaSerializer(serializers.ModelSerializer):
    type = AntennaTypeSerializer(read_only=True)
    images = AntennaGalleryReadSerializer(many=True)
    documents = AntennaDocumentReadSerializer(many=True)
    details = AntennaDetailSerializer(many=True)

    class Meta:
        model = Antenna
        fields = '__all__'
