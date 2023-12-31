# Generated by Django 4.2.2 on 2023-10-29 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0040_alter_classperiod_duration'),
        ('institution', '0004_branch_institution'),
        ('student', '0010_rename_institution_student_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEnroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(max_length=15, verbose_name='Class Roll')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classname', verbose_name='Class Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_enroll_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.section', verbose_name='Section')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.session', verbose_name='Session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student', verbose_name='Student')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_enroll_update_by', to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.version', verbose_name='version')),
            ],
            options={
                'db_table': 'st_enroll',
            },
        ),
    ]
