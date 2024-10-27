# Generated by Django 4.2.2 on 2024-10-24 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('setup_app', '0052_activestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Counter Code')),
                ('name', models.CharField(max_length=100, verbose_name='Counter Name')),
                ('counter_width', models.IntegerField(blank=True, null=True)),
                ('fiscal_year_as_prefix', models.BooleanField(default=False)),
                ('prefix', models.CharField(blank=True, max_length=20, null=True)),
                ('separator', models.CharField(blank=True, max_length=2, null=True)),
                ('step', models.IntegerField(default=1)),
                ('next_number', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sys_counter_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sys_counter_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'setup_sys_counter',
            },
        ),
    ]