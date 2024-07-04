import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import models as account_models
from accounts import serializers as account_serializers

logger = logging.getLogger(__name__)


class GetVerifiersView(APIView):
    def get(self, request, post_token):
        try:
            post = account_models.Post.objects.get(divar_post_id=post_token)
        except account_models.Post.DoesNotExist:
            return Response("error: Post not found", status=status.HTTP_404_NOT_FOUND)
        verifiers = post.selected_verifiers.all()
        serializer = account_serializers.VerifierSerializer(verifiers, many=True)
        return Response(data={"verifiers": serializer.data}, status=status.HTTP_200_OK)


class SetVerifiersView(APIView):
    def post(self, request, post_token):
        try:
            post = account_models.Post.objects.get(divar_post_id=post_token)
        except account_models.Post.DoesNotExist:
            return Response("error: Post not found", status=status.HTTP_404_NOT_FOUND)
        try:
            selected_verifiers = request.data["selected_verifiers"]
            verifiers = account_models.Verifier.objects.filter(id__in=selected_verifiers)
            for verifier in verifiers:
                post.verifiers.add(verifier)

            post.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"set verification error {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
