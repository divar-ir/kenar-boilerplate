from django.urls import path

from . import views

urlpatterns = [
    path("<uuid: survey_id>/", views.RateView, name="rating"),
]
