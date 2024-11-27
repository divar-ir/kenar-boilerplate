from django.contrib import admin

from addon.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
