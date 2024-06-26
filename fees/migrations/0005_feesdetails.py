# Generated by Django 4.2.2 on 2024-02-25 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fees', '0004_feesmaster'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeesDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('fine_type', models.IntegerField(blank=True, choices=[(0, 'None'), (1, 'Percentage'), (2, 'Fix Amount')], null=True)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Percentage %')),
                ('fix_amt', models.PositiveIntegerField(blank=True, null=True, verbose_name='Fix Amount')),
                ('description', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fees_dtl_creator', to=settings.AUTH_USER_MODEL)),
                ('fees_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees.feestype')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fees_dtl_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fe_fees_dtl',
            },
        ),
    ]
