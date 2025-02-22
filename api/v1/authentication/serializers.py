from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class SignUpProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


class SignUpUserSerializer(serializers.ModelSerializer):
    profile = SignUpProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        profile_serializer = SignUpProfileSerializer(instance=user.profile, data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            raise serializers.ValidationError(profile_serializer.errors)
        return user