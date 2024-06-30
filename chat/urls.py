from django.urls import path

from . import views

urlpatterns = [
    path("start_chat_session", views.start_chat_session, name="start_chat_session"),
    path("chat_oauth", views.chat_oauth, name="chat_oauth"),
    path("", views.chat_app, name="chat_app"),
    path("receive_notify", views.receive_notify, name="receive_notify"),
]
