from rest_framework import serializers

from documents.models import AntennaDocument


class AntennaDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntennaDocument
        fields = '__all__'
