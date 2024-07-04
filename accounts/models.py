from django.db import models
from oauth import models as oauth_models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampModel):
    username = models.CharField(max_length=50, unique=True)
    divar_user_phone = models.CharField(max_length=12, null=True, blank=True, unique=True)
    oauth = models.ForeignKey(to=oauth_models.OAuth, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Seller(TimestampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return f'Seller: {self.user.username}'


class Verifier(TimestampModel):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rate = models.DecimalField(default=5.0, max_digits=12)
    transactions_participated_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Verifier: {self.firstname} {self.lastname}'


class Post(TimestampModel):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    divar_post_id = models.IntegerField()
    selected_verifiers = models.ManyToManyField(Verifier)

    def __str__(self):
        return f'Post: {self.divar_post_id} by {self.seller.user.username}'

# Create your models here.
