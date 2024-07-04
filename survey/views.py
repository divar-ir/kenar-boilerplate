from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from matching.models import Transaction
from .models import Survey
from accounts.models import Verifier
from django.db.models import Avg
import decimal

class RateView(APIView):
    def post(self, request, survey_id):
        survey = get_object_or_404(Survey, uuid=survey_id)
        if survey.completed:
            return Response(data={"error": "Not Valid Survey"}, status=status.HTTP_400_BAD_REQUEST)
        rate = request.data.get('rate')
        survey.rate = decimal.Decimal(rate)
        survey.completed = True
        survey.save()

        avg_rate = Survey.objects.filter(target_verifier=survey.target_verifier).aggregate(Avg('rate'))['rate__avg']
        survey.target_verifier.rate = avg_rate
        survey.target_verifier.save()

        return Response(data={"message": "OK", "avg_rate": avg_rate}, status=status.HTTP_201_CREATED)
    def get(self, request, survey_id):

        survey = get_object_or_404(Survey, uuid=survey_id)

        if survey.completed:
            return Response(data={"status": "completed"})
        
        data = {
            "status": "open", 
            "verifier_name": survey.target_verifier.firstname + " " + survey.target_verifier.lastname,
            "post_id": survey.transaction.post.pk, 
        }

        return Response(data=data)
