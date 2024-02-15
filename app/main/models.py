from django.db import models
from django.conf import settings


class Transaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Transaction from {self.sender} to {self.receiver} amount {self.amount}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits = 10, decimal_places=2, default = 10000)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
     