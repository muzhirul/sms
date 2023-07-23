# Generated by Django 4.2.2 on 2023-07-23 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admission', '0009_admissiontestsetup'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmissionTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, choices=[('BANGLA', 'Bangla'), ('MATH', 'Math'), ('ENGLISH', 'English'), ('O', 'Other')], max_length=20, null=True)),
                ('mark', models.IntegerField(blank=True, null=True, verbose_name='Mark')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admission.admission')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ad_test_result_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ad_test_result_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ad_test_result',
            },
        ),
    ]
