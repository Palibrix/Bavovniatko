from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
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