# Generated by Django 4.0.6 on 2022-07-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_transactions_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='Transaction_exit_date',
        ),
        migrations.AddField(
            model_name='transactions',
            name='transaction_exit_date',
            field=models.DateTimeField(null=True),
        ),
    ]