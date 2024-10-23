from rest_framework import serializers

from components.models import Propeller


class PropellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Propeller
        fields = '__all__'
