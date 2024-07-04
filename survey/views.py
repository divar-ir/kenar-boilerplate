from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from matching.models import Transaction
from .models import Survey
from accounts.models import Verifier
from django.db.models import Avg

class RateView(APIView):
    def post(request, id):
        survey = get_object_or_404(Survey, id=id)
        
        rate = request.data.get('rate')
        survey.rate = rate
        survey.completed = True
        survey.save()

        survey.target_verifier.rate = Survey.objects.filter(target_verifier=survey.target_verifier).aggregate(Avg('rate'))
        survey.target_verifier.save()

        return Response(status=status.HTTP_201_CREATED)
    