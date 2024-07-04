from django.contrib import admin
from .models import VerificationRequest, Transaction
admin.site.register(VerificationRequest)
admin.site.register(Transaction)
