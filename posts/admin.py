from django.contrib import admin

from posts.models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["created_at"]
    filter = ["author"]


admin.site.register(Post, PostAdmin)
