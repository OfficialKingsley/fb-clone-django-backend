from .serializers import UserSerializer


def get_user(queryset):
    serializer = UserSerializer(queryset, read_only=True)
    return serializer.data
