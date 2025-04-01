from rest_framework import serializers

from components.models import Battery


class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = '__all__'


class BatteryWriteSerializer(serializers.ModelSerializer):
    """Write serializer for creating and updating batteries"""

    class Meta:
        model = Battery
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']