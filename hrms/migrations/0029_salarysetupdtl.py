# Generated by Django 4.2.2 on 2024-08-20 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hrms', '0028_salarysetupmst'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalarySetupDtl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Fixed Amount')),
                ('formula', models.CharField(blank=True, max_length=255, null=True)),
                ('min_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Minimum Amount')),
                ('max_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Max Amount')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch', verbose_name='Branch Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sal_stp_dtl_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('payroll_ele', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.payrollelement')),
                ('salary_setup_mst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.salarysetupmst')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sal_stp_dtl_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hrms_salary_setup_dtl',
            },
        ),
    ]
