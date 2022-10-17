from django.urls import path
from .views import DislikeView, LikeView, LikesView, PostView, PostsView


urlpatterns = [
    path("", PostsView.as_view(), name="all-posts"),
    path("<str:id>/dislike/", DislikeView.as_view(), name="dislike-post"),
    path("<str:id>/likes/", LikesView.as_view(), name="like-post"),
    path("<str:id>/like/", LikeView.as_view(), name="like-post"),
    path("<str:id>/", PostView.as_view(), name="single-post"),
]
