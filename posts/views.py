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


class LikesView(views.APIView):
    """This is the view to like"""

    def post(self, request, pk):
        """Here is the post view"""
        post = Post.objects.get(pk=pk)
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        post.likes.add(user)
        return Response("Like added")

    def get(self, request, pk):
        """Here is the get view"""

        post = Post.objects.get(pk=pk)
        serializer = LikeSerializer(post)
        likes = serializer.data
        return Response(likes)


class DislikeView(views.APIView):
    """This is the view to like"""

    def post(self, request, pk):
        """Here is the like or dislike view"""

        post = Post.objects.get(pk=pk)
        user = request.data.get("user_id")
        post.likes.remove(user)
