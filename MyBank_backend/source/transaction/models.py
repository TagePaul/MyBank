from django.db import models
from user.models import Bank_Account
from django.core import validators

class Transactions(models.Model):
    STATUS = [
        ('cancelled', 'cancelled'),
        ('in_process', 'in_process',),
        ('success', 'success')
    ]
    transaction_id = models.BigIntegerField(unique=True, 
                        verbose_name='id транзакции',
                        null=False)
    transfer_from_bank_account = models.ForeignKey(Bank_Account, 
                        on_delete=models.CASCADE, null=False,
                        related_name='outgoing_transfers')
    transfer_to_bank_account = models.ForeignKey(Bank_Account, 
                        on_delete=models.CASCADE, null=False,
                        related_name='incoming_transfers')
    status = models.CharField(null=False, 
                        max_length=99,
                        choices=STATUS, 
                        verbose_name='Статус транзакции')
    transfer_amount = models.IntegerField(null=False, 
                        validators=[validators.MinValueValidator(1)])
    transaction_start_date = models.DateTimeField(
                        auto_now_add=True)
    transaction_exit_date = models.DateTimeField(null=True)