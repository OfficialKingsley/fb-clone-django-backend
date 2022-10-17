from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from core.choices import theme_choices
from django.conf import settings

from posts.models import Post

UserModel = settings.AUTH_USER_MODEL

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        password=None,
        **extra_fields,
    ):
        """Method for creating user"""
        if not email:
            raise ValueError("Email is Required")
        if not first_name:
            raise ValueError("First Name is Required")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff user must have is_staff=True")

        user = self.create_user(
            email=email,
            first_name=first_name,
            password=password,
            **extra_fields,
        )
        return user

    def create_superuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff user must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        user = self.create_user(
            email=email,
            first_name=first_name,
            password=password,
            **extra_fields,
        )
        return user


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
        if len(self.last_name) > 0 and len(self.middle_name) > 0:
            return f"{self.first_name} ({self.middle_name}) {self.last_name}"
        elif len(self.last_name) <= 0 and len(self.middle_name) > 0:
            return f"{self.first_name} ({self.middle_name})"
        elif len(self.last_name) > 0 and len(self.middle_name) <= 0:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name}"

    @property
    def posts(self):
        user_posts = Post.objects.filter(id=self.id).first()
        return user_posts

    def get_short_name(self):
        return self.first_name

    # Permissions
    def has_perms(self, perm, obj=None):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

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
