# Generated by Django 4.2.2 on 2024-03-16 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0200_alter_classsubject_book_file'),
        ('staff', '0049_alter_staffleavetransaction_app_status'),
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0007_alter_examroutine_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoutineMst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('class_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.classname')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exam_routine_mst_creator', to=settings.AUTH_USER_MODEL)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.examname')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.classgroup')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.section')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.session')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exam_routine_mst_update_by', to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.version')),
            ],
            options={
                'db_table': 'e_routine_mst',
            },
        ),
        migrations.CreateModel(
            name='ExamRoutineDtl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.DateField()),
                ('day', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Exam Day')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('duration', models.DurationField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exam_routine_dtl_creator', to=settings.AUTH_USER_MODEL)),
                ('exam_routine_mst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_routine_dtl', to='exam.examroutinemst')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classroom')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.subject')),
                ('teacher', models.ManyToManyField(to='staff.staff', verbose_name='Teacher')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exam_routine_dtl_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'e_routine_dtl',
            },
        ),
    ]
