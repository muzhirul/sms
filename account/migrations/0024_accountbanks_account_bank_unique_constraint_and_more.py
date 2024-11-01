# Generated by Django 4.2.2 on 2024-10-30 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_alter_chartofaccounts_code_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='accountbanks',
            constraint=models.UniqueConstraint(fields=('bank_name', 'branch_name', 'account_no', 'status', 'institution', 'branch'), name='account_bank_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='accountperiod',
            constraint=models.UniqueConstraint(fields=('start_date', 'end_date', 'status'), name='account_preiod_unique_constraint'),
        ),
    ]
