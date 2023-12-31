# Generated by Django 4.2.2 on 2023-11-04 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('hrms', '0005_attendancedetail_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desig_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255, verbose_name='Designation Name')),
                ('dgroup_id', models.CharField(blank=True, max_length=10, null=True)),
                ('sdate', models.DateField(blank=True, null=True)),
                ('attn', models.IntegerField(blank=True, null=True)),
                ('holiday_allow', models.BooleanField(default=True)),
                ('night_allow', models.BooleanField(default=False)),
                ('tiffin_allow', models.BooleanField(default=False)),
                ('festival_allow', models.BooleanField(default=True)),
                ('sal_grade', models.IntegerField(blank=True, null=True)),
                ('work_type', models.CharField(blank=True, max_length=255, null=True)),
                ('ifter_allow', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='degi_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='degi_update_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
