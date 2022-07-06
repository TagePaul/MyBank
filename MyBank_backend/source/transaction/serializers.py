from django.contrib.auth import get_user_model
from django.core import validators
from rest_framework import serializers

from .models import Transactions

User = get_user_model()

class TransactionSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)
    transfer_amount = serializers.IntegerField(
                    validators=[validators.MinValueValidator(1)])


class My_transactionsSerializer(serializers.ModelSerializer):
    transfer_from_bank_account = serializers.StringRelatedField()
    transfer_to_bank_account = serializers.StringRelatedField()

    class Meta:
        model = Transactions
        fields = ('__all__')
