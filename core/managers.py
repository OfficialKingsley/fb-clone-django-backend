from django.contrib.auth.models import BaseUserManager


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
