from rest_framework import serializers

from components.models import RatedVoltage, MotorDetail, Motor


class RatedVoltageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatedVoltage
        fields = '__all__'


class MotorDetailSerializer(serializers.ModelSerializer):
    voltage = RatedVoltageSerializer(read_only=True)

    class Meta:
        model = MotorDetail
        fields = '__all__'


class MotorSerializer(serializers.ModelSerializer):
    details = MotorDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Motor
        fields = '__all__'