"""Serializers for our post models"""

from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Post serializer for managing post views"""

    # image = serializers.Hyperlink()
    class Meta:
        """Meta information about the post serializer"""

        model = Post
        fields = [
            "id",
            "author",
            "text",
            "image",
            "created_at",
            "updated_at",
            "number_of_likes",
            "likes",
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        """Some Meta Info"""

        model = Post
        fields = ["likes"]
