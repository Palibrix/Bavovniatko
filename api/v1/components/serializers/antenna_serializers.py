from rest_framework import serializers

from api.v1.documents.serializers import AntennaDocumentSerializer
from api.v1.galleries.serializers import AntennaGallerySerializer
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
    gallery = AntennaGallerySerializer(many=True, read_only=True)
    document = AntennaDocumentSerializer(many=True, read_only=True)
    details = AntennaDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Antenna
        fields = '__all__'
