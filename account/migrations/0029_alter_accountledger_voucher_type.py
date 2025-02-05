# Generated by Django 4.2.2 on 2025-01-06 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_alter_accountledger_voucher_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountledger',
            name='voucher_type',
            field=models.CharField(choices=[('PAYMENT', 'Payment'), ('RECEIVE', 'Receive'), ('JOURNAL', 'Journal'), ('PURCHASE', 'Purchase'), ('SUPPLIER PAYMENT', 'Supplier Payment')], max_length=30),
        ),
    ]
