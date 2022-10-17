"""This is the models.py file for the posts"""

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Create your models here.
class Post(models.Model):
    """This is a post model"""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to="images/posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    @property
    def number_of_likes(self):
        """Returns the number of likes"""
        return self.likes.count()

    class Meta:
        """Meta information about the post model"""

        ordering = ["updated_at"]
        verbose_name = "post"
        verbose_name_plural = "posts"
