from rest_framework import serializers

from api.v1.users.serializers import UserSerializer


class BaseSuggestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        abstract = True
        read_only_fields = ['id', 'user', 'status', 'admin_comment']
