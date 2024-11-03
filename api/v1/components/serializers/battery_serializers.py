from rest_framework import serializers

from components.models import Battery


class BatterySerializer(serializers.Serializer):
    class Meta:
        model = Battery
        fields = '__all__'