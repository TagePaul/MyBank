# Generated by Django 4.0.6 on 2022-07-06 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='transaction_id',
            field=models.BigIntegerField(unique=True, verbose_name='id транзакции'),
        ),
    ]