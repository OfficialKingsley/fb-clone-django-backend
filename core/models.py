from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Post

from core.choices import theme_choices
from core.managers import UserManager

UserModel = get_user_model()

# Create your models here.


class User(AbstractBaseUser):
    """This is the custom user model"""

    class Meta:
        """Meta Information of User Model"""

        verbose_name = "user"
        verbose_name_plural = "users"

    email = models.EmailField(max_length=150, unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, default="", blank="True")
    last_name = models.CharField(max_length=150, default="", blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="images/users",
        blank=True,
        default="images/users/default.png",
    )
    cover_image = models.ImageField(
        upload_to="images/users/cover",
        blank=True,
        default="images/users/cover/default.png",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # TODO: this should be handled as session/cookie on the frontend
    theme = models.CharField(max_length=15, choices=theme_choices, default="dark")
    friends = models.ManyToManyField(
        UserModel,
        related_name="Friends",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def get_full_name(self):
        return f"{self.first_name} ({self.middle_name}) {self.last_name}"

    @property
    def full_name(self):
        first_name = self.first_name or ""
        middle_name = self.middle_name or ""
        last_name = self.last_name or ""

        return f"{first_name} {middle_name} {last_name}"

    @property
    def posts(self):
        user_posts = Post.objects.filter(id=self.id).first()
        return user_posts

    def get_short_name(self):
        return self.first_name

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} ({self.id})"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="friend_request_sender"
    )
    receiver = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="friend_request_receiver"
    )
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.first_name} to {self.receiver.first_name}"


class Notification(models.Model):
    user_for = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    read_state = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message} - Message for {self.user_for.full_name}"
