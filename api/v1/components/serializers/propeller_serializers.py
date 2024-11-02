from rest_framework import serializers

from api.v1.documents.serializers import PropellerDocumentSerializer
from api.v1.galleries.serializers import PropellerGallerySerializer
from components.models import Propeller


class PropellerSerializer(serializers.ModelSerializer):
    images = PropellerGallerySerializer(many=True)
    documents = PropellerDocumentSerializer(many=True)

    class Meta:
        model = Propeller
        fields = '__all__'
