from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.forms import UserAdminCreationForm, UserAdminChangeForm
from core.models import FriendRequest, Notification

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    """The forms to add and change user instances"""

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["first_name", "email", "is_active", "is_admin"]
    list_filter = ["is_admin", "is_staff", "is_active"]
    fieldsets = (
        (
            "Intro",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "date_of_birth",
                )
            },
        ),
        ("Relationships", {"fields": ("friends",)}),
        (
            "Preferences",
            {
                "fields": (
                    "theme",
                    "profile_image",
                    "cover_image",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "password", "password2"),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["first_name", "middle_name", "last_name", "date_of_birth"]
    filter_horizontal = ()


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "accepted"]
    list_filter = ["sender", "receiver", "accepted"]
    search_fields = ["sender", "receiver", "accepted"]


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user_for", "message", "read_state"]
    list_filter = ["user_for", "message", "read_state"]
    search_fields = ["user_for", "message", "read_state"]


admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Notification, NotificationAdmin)
