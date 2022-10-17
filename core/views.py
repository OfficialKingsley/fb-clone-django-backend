# from django.shortcuts import render
# from django.conf import settings

from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.response import Response
from core.models import FriendRequest, Notification
from core.serializers import (
    FriendRequestSerializer,
    NotificationSerializer,
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from .functions import get_user

from posts.models import Post
from posts.serializers import PostSerializer

User = get_user_model()


# Create your views here.
class UsersView(views.APIView):
    """This is the view to get all the users"""

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(views.APIView):
    """View To Get A Single User"""

    def get(self, request, id):
        queryset = User.objects.get(id=id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    # def put(self, request, id):


class RegisterView(views.APIView):

    """This is the view to register"""

    serializer_class = RegisterSerializer

    def post(self, request):
        """This is the post function for the register view"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, request):
        return Response({"message": "Get Request Not Allowed"})


class LoginView(views.APIView):
    """This is the view to login"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            queryset = User.objects.filter(email=request.data["email"]).first()
            user = get_user(queryset)
            serializer.save()
            return Response(user)
        return Response(serializer.errors)


class LogoutView(views.APIView):
    def post(self, request, id):
        user = User.objects.filter(id=id).first()
        user.is_active = False
        user.save()
        return Response({"message": "Successfully logged out"})


class PostsView(views.APIView):
    def get(self, request, id):
        postData = Post.objects.filter(author=id)
        serializer = PostSerializer(postData, many=True)
        posts = serializer.data
        return Response(posts)


class FriendRequestsView(views.APIView):
    def get(self, request, id):
        queryset = FriendRequest.objects.filter(receiver=id)
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class SentRequestsView(views.APIView):
    def get(self, request, id):
        queryset = FriendRequest.objects.filter(sender=id)
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class FriendRequestView(views.APIView):
    serializer_class = FriendRequestSerializer

    def post(self, request, id):
        serializer = FriendRequestSerializer(data=request.data)
        sender_id = request.data.get("sender")
        user_sender = User.objects.get(id=sender_id)
        user_receiver = User.objects.get(id=id)
        notification = Notification(
            user_for=user_receiver,
            message=f"{user_sender.full_name} just sent you a friend request",
        )
        if serializer.is_valid():
            serializer.save()
            notification.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class AcceptRequestView(views.APIView):
    def post(self, request, id, request_id):
        print("The id is", id)
        friend_request = FriendRequest.objects.filter(id=request_id).first()
        friend_request.accepted = True
        user_sender = User.objects.get(id=friend_request.sender.id)
        user_receiver = User.objects.get(id=friend_request.receiver.id)
        user_sender.friends.add(user_receiver.id)
        user_receiver.friends.add(user_sender.id)
        notification = Notification(
            user_for=user_sender,
            message=f"{user_receiver.full_name} has accepted your friend request",
        )
        notification.save()
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)


class DeclineRequestView(views.APIView):
    def post(self, request, id, request_id):
        friend_request = FriendRequest.objects.filter(id=request_id).first()
        if friend_request.accepted == True:
            return Response({"Message": "You have already accepted this request"})
        friend_request.delete()
        return Response({"Message": "Request Has Been Deleted"})


class NotificationsView(views.APIView):
    def get(self, request, id):
        notifications = Notification.objects.filter(user_for=id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
