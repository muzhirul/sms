# Generated by Django 4.2.2 on 2024-10-30 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0038_accounttaxdtl_pct_alter_accounttaxdtl_lmt'),
        ('account', '0025_accountvouchermaster_account_ledger_unique_constraint'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='accountbanks',
            name='account_bank_unique_constraint',
        ),
        migrations.RemoveField(
            model_name='accountbanks',
            name='bank_name',
        ),
        migrations.AddField(
            model_name='accountbanks',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.accountbank', verbose_name='Bank Name'),
        ),
    ]