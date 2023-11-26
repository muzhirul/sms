# Generated by Django 4.2.2 on 2023-11-26 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import setup_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('setup_app', '0038_contracttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[setup_app.models.validate_alpha_chars_only], verbose_name='Marital Status')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marital_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marital_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 's_marital_status',
            },
        ),
    ]
