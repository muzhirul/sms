# Generated by Django 4.2.2 on 2024-12-01 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase', '0012_alter_supplier_current_amt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierPaymentMst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment Number')),
                ('pay_date', models.DateTimeField()),
                ('total_pay_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Payment Amount')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sup_pay_mst_creator', to=settings.AUTH_USER_MODEL)),
                ('grn_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.goodsreceiptnotemaster', verbose_name='GRN Code')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.supplier')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sup_pay_mst_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Supplier Payment',
                'db_table': 'pur_supplier_payment_mst',
            },
        ),
    ]
