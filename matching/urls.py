from django.urls import include, path

from matching import views

urlpatterns = [
    path("getVerifiers/<int:post_token>", views.GetVerifiersView.as_view(), name="get_verifiers")
]
