"""Views for my posts"""

from rest_framework import views
from rest_framework.response import Response

from .models import Post
from .serializers import LikeSerializer, PostSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


class PostsView(views.APIView):
    """This is the view to get and add posts"""

    serializer_class = PostSerializer

    def get(self, request):
        """This is the get method for the posts view"""
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a post"""
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class PostView(views.APIView):
    """Single Post View"""

    serializer_clas = PostSerializer

    def get(self, request, id):
        """Getting Single Post"""

        queryset = Post.objects.get(id=id)
        serializer = PostSerializer(queryset)
        return Response(serializer.data)


class LikeView(views.APIView):
    """This is the view to like"""

    def post(self, request, id):
        """Here is the post view"""
        post = Post.objects.get(id=id)
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        post.likes.add(user)
        return Response("Like added")


class DislikeView(views.APIView):
    """This is the view to like"""

    def post(self, request, id):
        """Here is the post view"""
        post_object = Post.objects.get(id=id)
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        post_object.likes.remove(user)
        return Response("Like removed")


class LikesView(views.APIView):
    """This is the view to like"""

    def get(self, request, id):
        """Here is the get view"""

        post = Post.objects.get(id=id)
        serializer = LikeSerializer(post)
        return Response(serializer.data)
