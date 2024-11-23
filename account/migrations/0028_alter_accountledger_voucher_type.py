# Generated by Django 4.2.2 on 2024-11-21 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_accountbanks_account_bank_unique_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountledger',
            name='voucher_type',
            field=models.CharField(choices=[('PAYMENT', 'Payment'), ('RECEIVE', 'Receive'), ('JOURNAL', 'Journal'), ('PURCHASE', 'Purchase')], max_length=30),
        ),
    ]