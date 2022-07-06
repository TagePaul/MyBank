from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User,
                related_name='profile',
                on_delete=models.CASCADE, 
                null=False)
    city = models.CharField(max_length=300, 
                null=False, 
                verbose_name='Город')
    creation_date = models.DateField(auto_now_add=True, 
                verbose_name='Дата создания')


class Bank_Account(models.Model):
    profile = models.ForeignKey(Profile, 
                on_delete=models.PROTECT, 
                related_name='bank_accounts', 
                null=False)
    phone_number = models.CharField(max_length=30, 
                null=False, 
                unique=True, verbose_name='Номер телефона')
    number_account = models.CharField(max_length=30, 
                null=False, 
                unique=True,
                verbose_name='Номер счёта')
    balance = models.IntegerField(default=0, 
                null=False, 
                verbose_name='Баланс',
                validators=[validators.MinValueValidator(0)])
    status = models.BooleanField(default=True,
                verbose_name='Статус',
                null=False)
    creation_date = models.DateField(auto_now_add=True,
                verbose_name='Дата создания')

    def __str__(self):
        return self.number_account
    