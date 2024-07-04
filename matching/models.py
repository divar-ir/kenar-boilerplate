from django.db import models
from accounts import models as accounts_models


class VerificationRequest(accounts_models.TimestampModel):
    class Status(models.IntegerChoices):
        BUYER_CLAIMED = 1, 'Buyer Claimed'
        SELLER_APPROVED = 2, 'Seller Approved'
        SELLER_REJECTED = 3, 'Seller Rejected'

    seller = models.ForeignKey(to=accounts_models.Seller, on_delete=models.CASCADE)
    claimed_buyer = models.ForeignKey(to=accounts_models.User, related_name='claimed_buyer', on_delete=models.CASCADE)
    verifier = models.ForeignKey(to=accounts_models.Verifier, on_delete=models.CASCADE)
    post = models.ForeignKey(to=accounts_models.Post, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=Status.choices)

    def __str__(self):
        return f'VerificationRequest: {self.id}'


class Transaction(accounts_models.TimestampModel):
    class Status(models.IntegerChoices):
        PENDING = 1, 'Pending'
        MANUALLY_CLOSED = 2, 'Manually Closed'
        APPROVED = 3, 'Approved'
        DISAPPROVED = 4, 'Disapproved'

    seller = models.ForeignKey(to=accounts_models.Seller, on_delete=models.CASCADE)
    post = models.ForeignKey(to=accounts_models.Post, on_delete=models.CASCADE)
    buyer = models.ForeignKey(to=accounts_models.User, related_name='buyer', on_delete=models.CASCADE)
    verifier = models.ForeignKey(to=accounts_models.Verifier, on_delete=models.CASCADE)
    verification_request = models.ForeignKey(to=VerificationRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=Status.choices)

    def __str__(self):
        return f'Transaction: {self.id}'
# Create your models here.
