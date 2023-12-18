# Generated by Django 4.2.2 on 2023-12-18 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields
import staff.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('hrms', '0014_leavetype_is_active'),
        ('staff', '0037_attendancedailyraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffLeaveTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=staff.models.leave_code, editable=False, max_length=20, null=True, verbose_name='Leave Code')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('tran_type', models.CharField(blank=True, max_length=20, null=True)),
                ('day_count', models.DurationField(blank=True, null=True)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('add_during_leave', models.TextField(blank=True, null=True)),
                ('reason_for_leave', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('app_status', models.CharField(blank=True, max_length=20, null=True)),
                ('active_start_date', models.DateTimeField(blank=True, null=True)),
                ('active_end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('apply_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apply_by', to='staff.staff')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch', verbose_name='Branch Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_trns_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('leave_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.leavetype')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resonsible_by', to='staff.staff')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_trns_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'staff_leave_trns',
            },
        ),
    ]
