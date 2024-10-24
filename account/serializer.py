from rest_framework import serializers
from .models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_student",
            "field",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        fields = ["uid", "image", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.get_or_create(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile
