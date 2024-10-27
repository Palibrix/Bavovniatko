from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer
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
    details = ReceiverDetailSerializer(many=True, read_only=True)
    protocols = ReceiverProtocolTypeSerializer(many=True, read_only=True)
    antenna_connectors = AntennaConnectorSerializer(many=True, read_only=True)

    class Meta:
        model = Receiver
        fields = '__all__'