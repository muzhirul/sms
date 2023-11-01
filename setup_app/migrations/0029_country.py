# Generated by Django 4.2.2 on 2023-11-01 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import setup_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('setup_app', '0028_alter_district_name_alter_educationboard_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dist_code', models.CharField(max_length=4, verbose_name='Country Code')),
                ('name', models.CharField(max_length=50, validators=[setup_app.models.validate_alpha_chars_only], verbose_name='Country Name')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch', verbose_name='Branch Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 's_country',
            },
        ),
    ]
