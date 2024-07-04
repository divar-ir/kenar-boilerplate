from django.db import models
from accounts import models as accounts_models
from matching import models as matching_models
from django.db import models
import uuid, base64

class Side(models.IntegerChoices):
        BUYER = 1, 'Buyer'
        SELLER = 2, 'Seller'

def generate_short_uuid():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('ascii')[:12]

class Survey(models.Model):
    uuid = models.CharField(default=generate_short_uuid, editable=False, unique=True, max_length=12)
    side = models.SmallIntegerField(choices=Side.choices)

    rating_user = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    target_verifier = models.ForeignKey(accounts_models.Verifier, on_delete=models.CASCADE)
    transaction = models.ForeignKey(matching_models.Transaction, on_delete=models.CASCADE)

    rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)


    completed = models.BooleanField(default=False)

    def __str__(self):
         return f'Survey {self.uuid}'
    
    
