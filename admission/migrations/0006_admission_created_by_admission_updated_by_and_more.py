# Generated by Django 4.2.2 on 2023-07-23 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admission', '0005_guardian'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='created_by',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admission_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='admission',
            name='updated_by',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admission_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guardian',
            name='created_by',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guardian_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guardian',
            name='updated_by',
            field=django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guardian_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='ocupation',
            field=models.CharField(blank=True, choices=[('DOCTOR', 'Doctor'), ('TEACHER', 'Teacher'), ('OTHER', 'Other')], max_length=10, null=True, verbose_name='Ocupation'),
        ),
    ]
