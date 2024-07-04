from django.urls import path

from . import views

urlpatterns = [
    path("<uuid:survey_id>/", views.RateView.as_view(), name="rating"),
]
