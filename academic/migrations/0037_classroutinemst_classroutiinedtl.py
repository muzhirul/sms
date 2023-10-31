# Generated by Django 4.2.2 on 2023-10-19 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_staff_department_staff_designation_staff_shift'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('setup_app', '0021_subjecttype'),
        ('academic', '0036_alter_subject_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoutineMst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classname', verbose_name='Class Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_routine_mst_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.section', verbose_name='Section')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.session', verbose_name='Session')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_routine_mst_update_by', to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.version', verbose_name='Version')),
            ],
            options={
                'db_table': 'ac_class_routine_mst',
            },
        ),
        migrations.CreateModel(
            name='ClassRoutiineDtl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classperiod', verbose_name='Class Period')),
                ('class_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.classroom', verbose_name='Class Room')),
                ('class_routine_mst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routine_dtl', to='academic.classroutinemst')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_routine_dtl_creator', to=settings.AUTH_USER_MODEL)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup_app.day', verbose_name='Day')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.subject', verbose_name='Subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff', verbose_name='Teacher Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_routine_dtl_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ac_class_routine_dtl',
            },
        ),
    ]