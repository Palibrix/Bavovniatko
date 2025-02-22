from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer
from api.v1.documents.serializers import ReceiverDocumentReadSerializer
from api.v1.galleries.serializers import ReceiverGalleryReadSerializer
from components.models import Motor, ReceiverProtocolType, ReceiverDetail, Receiver


class ReceiverProtocolTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiverProtocolType
        fields = '__all__'


class ReceiverDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiverDetail
        fields = '__all__'


class ReceiverSerializer(serializers.ModelSerializer):
    details = ReceiverDetailSerializer(many=True)
    protocols = ReceiverProtocolTypeSerializer(many=True)
    antenna_connectors = AntennaConnectorSerializer(many=True)
    images = ReceiverGalleryReadSerializer(many=True)
    documents = ReceiverDocumentReadSerializer(many=True)

    class Meta:
        model = Receiver
        fields = '__all__'
