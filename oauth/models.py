import uuid

from django.db import models
from django.utils.timezone import now

from addon.models import Post
from chat.models import Chat


class OAuth(models.Model):
    session_id = models.CharField(max_length=128, unique=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    expires_in = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="oauths")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True, related_name="oauths")
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return now() >= self.expires_in

    def __str__(self):
        return self.session_id
