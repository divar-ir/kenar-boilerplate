from django.urls import path

from . import views

urlpatterns = [
    path("callback/", views.oauth_callback, name="oauth-callback"),
]
