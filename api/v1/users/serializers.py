from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')
        read_only_fields = ('user', 'id',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            nested_serializer = self.fields['profile']
            nested_instance = Profile.objects.get(user=instance)
            nested_data = validated_data.pop('profile')
            nested_serializer.update(nested_instance, nested_data)

        user = super().update(instance, validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    lists_count = serializers.SerializerMethodField()
    suggestions_count = serializers.SerializerMethodField()
    drones_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'lists_count', 'suggestions_count', 'drones_count']

    def get_lists_count(self, obj):
        return obj.lists.count()

    def get_suggestions_count(self, obj):
        # This is a placeholder counting only one type of suggestion
        # In a full implementation, we would aggregate all suggestion types
        return 0

    def get_drones_count(self, obj):
        return obj.drone_set.count() if hasattr(obj, 'drone_set') else 0


class UserPublicProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        if profile_data:
            profile = instance.profile
            profile.first_name = profile_data.get('first_name', profile.first_name)
            profile.last_name = profile_data.get('last_name', profile.last_name)
            profile.save()

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance