from django.db import models
from accounts import models as accounts_models
from matching import models as matching_models


class RateEvent(accounts_models.TimestampModel):
    class Side(models.IntegerChoices):
        BUYER = 1, 'Buyer'
        SELLER = 2, 'Seller'

    transaction = models.ForeignKey(matching_models.Transaction, on_delete=models.CASCADE)
    rating_user = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    side = models.SmallIntegerField(choices=Side.choices)

    def __str__(self):
        return f'RateEvent: {self.id}'
# Create your models here.
