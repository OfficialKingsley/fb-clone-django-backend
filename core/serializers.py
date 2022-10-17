"""Serializers for the core/user module"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import FriendRequest, Notification

from posts.models import Post

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


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer to register a user"""

    password = serializers.CharField(
        max_length=150, required=True, write_only=True, min_length=8
    )
    password2 = serializers.CharField(
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
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords Didn't match")
        if not attrs["first_name"]:
            raise ValueError("First name is Required")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            middle_name=validated_data["middle_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        try:
            user = User.objects.filter(email=email).first()
            if user is not None:
                if user.check_password(password):
                    user.is_active = True
                    user.save()
                    return user
                else:
                    raise ValueError("Incorrect Password")
        except ObjectDoesNotExist:
            raise ModuleNotFoundError("User not found")


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
