from django.urls import path
from .views import LikesView, PostsView


urlpatterns = [
    path("", PostsView.as_view(), name="all-posts"),
    path("<str:pk>/like/", LikesView.as_view(), name="like-post"),
]
