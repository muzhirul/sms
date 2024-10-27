# Generated by Django 4.2.2 on 2024-10-23 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0017_accountledger_voucher_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountledger',
            name='voucher_type',
            field=models.CharField(choices=[('PAYMENT', 'Payment'), ('RECEIVE', 'Receive'), ('JOURNAL', 'Journal')], max_length=30),
        ),
        migrations.CreateModel(
            name='AccountVoucherMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.CharField(blank=True, max_length=50, null=True)),
                ('voucher_type', models.CharField(choices=[('PAYMENT', 'Payment'), ('RECEIVE', 'Receive'), ('JOURNAL', 'Journal')], max_length=30)),
                ('gl_date', models.DateField(auto_now_add=True)),
                ('total_debit_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Debit Amount')),
                ('total_credit_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Credit Amount')),
                ('confirm', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acc_coa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acc_vou_coa', to='account.chartofaccounts')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acc_vou_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acc_vou_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'acc_voucher_mst',
            },
        ),
    ]