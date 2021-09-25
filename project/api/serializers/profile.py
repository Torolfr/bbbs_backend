from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='pk', read_only=True)

    class Meta:
        fields = ['id', 'user', 'city']
        model = User


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'email']
        model = User
