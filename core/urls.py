"""This is the url configuration of the core user app"""

from django.urls import path

from core.views import (
    AcceptRequestView,
    DeclineRequestView,
    FriendRequestView,
    FriendRequestsView,
    LoginView,
    LogoutView,
    NotificationsView,
    PostsView,
    RegisterView,
    SentRequestsView,
    UserView,
    UsersView,
)

urlpatterns = [
    path("", UsersView.as_view(), name="all-users"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("<str:id>/logout/", LogoutView.as_view(), name="logout"),
    path("<str:id>/posts/", PostsView.as_view(), name="user-posts"),
    path(
        "<str:id>/friend-requests/",
        FriendRequestsView.as_view(),
        name="send-friend-request",
    ),
    path(
        "<str:id>/friend-requests/<str:request_id>/accept/",
        AcceptRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "<str:id>/friend-requests/<str:request_id>/decline/",
        DeclineRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "<str:id>/sent-requests/",
        SentRequestsView.as_view(),
        name="send-friend-request",
    ),
    path(
        "<str:id>/add-friend/",
        FriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "<str:id>/notifications/",
        NotificationsView.as_view(),
        name="notifications",
    ),
    path("<str:id>/", UserView.as_view(), name="single-user"),
]
