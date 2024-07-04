from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from accounts.models import Verifier


class VerifierSerializer(ModelSerializer):
    rate = SerializerMethodField()

    class Meta:
        model = Verifier
        fields = '__all__'

    def get_rate(self, obj):
        return str(round(obj.rate, 2))
