from django.contrib import admin

from oauth.models import OAuth


@admin.register(OAuth)
class OAuthAdmin(admin.ModelAdmin):
    pass
