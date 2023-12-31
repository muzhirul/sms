# Generated by Django 4.2.2 on 2023-11-01 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('setup_app', '0021_subjecttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_code', models.CharField(max_length=3, verbose_name='Board Code')),
                ('name', models.CharField(max_length=50, verbose_name='Board Name')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch', verbose_name='Branch Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edu_board_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edu_board_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 's_edu_board',
            },
        ),
    ]
