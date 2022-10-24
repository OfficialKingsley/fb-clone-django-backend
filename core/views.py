from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.models import FriendRequest, Notification
from core.serializers import (
    FriendRequestSerializer,
    LoginSerializer,
    NotificationSerializer,
    RegisterSerializer,
    UserSerializer,
)

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

    # TODO:`IsObjectOwnerOrReadOnly`
    # Allows only the owner of the account to perform write operations
    # Allows unauthenticated users to view the account details

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get(self, request, id):
        queryset = get_object_or_404(User, id=id)
        serializer = UserSerializer(queryset)

        return Response(serializer.data)

    def put(self, request, id):
        queryset = get_object_or_404(User, id=id)

        serializer = UserSerializer(
            queryset,
            data=request.data,
            partial=True,
            context={"request": request},  # pass this to process files in serializer
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class RegisterView(views.APIView):

    """This is the view to register"""

    serializer_class = RegisterSerializer

    def post(self, request):
        """This is the post function for the register view"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    """This is the view to login"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # not sure it's needed

        login(request, serializer.instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)

        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT
        )


class PostsView(views.APIView):
    def get(self, request, id):
        postData = Post.objects.filter(author=id)
        serializer = PostSerializer(postData, many=True)
        posts = serializer.data
        return Response(posts)


class FriendRequestsView(views.APIView):

    # TODO: `IsObjectOwner`
    permission_classess = [IsAuthenticated]

    def get(self, request):
        id = request.user.id
        queryset = FriendRequest.objects.filter(receiver=id)
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class SentRequestsView(views.APIView):

    # TODO: `IsObjectOwner`
    permission_classess = [IsAuthenticated]

    def get(self, request):
        id = request.user.id

        queryset = FriendRequest.objects.filter(sender=id)
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class FriendRequestView(views.APIView):

    # TODO: `IsObjectOwner`
    permission_classess = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def post(self, request):
        id = request.user.id

        sender_id = request.data.get("sender")
        user_sender = User.objects.get(id=sender_id)
        user_receiver = User.objects.get(id=id)

        serializer = FriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        notification = Notification(
            user_for=user_receiver,
            message=f"{user_sender.full_name} just sent you a friend request",
        )
        notification.save()

        return Response(serializer.data)


class AcceptRequestView(views.APIView):

    # TODO: `IsObjectOwner`
    permission_classess = [IsAuthenticated]

    def post(self, request, request_id):
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

    # TODO: `IsObjectOwner`
    permission_classess = [IsAuthenticated]

    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)

        if friend_request.accepted == True:
            return Response({"Message": "You have already accepted this request"})
        friend_request.delete()

        return Response(
            {"Message": "Request Has Been Deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class NotificationsView(views.APIView):
    def get(self, request, id):
        notifications = Notification.objects.filter(user_for=id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
