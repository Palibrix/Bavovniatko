from rest_framework import serializers

from api.v1.documents.serializers import PropellerDocumentReadSerializer
from api.v1.galleries.serializers import PropellerGalleryReadSerializer
from components.models import Propeller


class PropellerSerializer(serializers.ModelSerializer):
    images = PropellerGalleryReadSerializer(many=True)
    documents = PropellerDocumentReadSerializer(many=True)

    class Meta:
        model = Propeller
        fields = '__all__'
