from rest_framework import serializers

from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from documents.models import AntennaDocument
from galleries.models import AntennaGallery


class AntennaGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaGallery
        fields = '__all__'
