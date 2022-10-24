"""Serializers for the core/user module"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import FriendRequest, Notification

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user"""

    class Meta:
        """Meta Information of the user serializer"""

        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "email",
            "date_of_birth",
            "profile_image",
            "cover_image",
            "friends",
            "theme",
        )

    # drf `get_<property_name>` method
    def get_full_name(self, obj: User):
        return obj.full_name


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer to register a user"""

    password = serializers.CharField(
        max_length=150, required=True, write_only=True, min_length=8
    )
    confirm_password = serializers.CharField(
        max_length=150, required=True, write_only=True, min_length=8
    )
    email = serializers.EmailField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email must be unique",
            )
        ],
    )

    class Meta:
        """Meta information for the register serializer"""

        model = User
        fields = [
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords Didn't match")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
