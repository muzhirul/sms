# Generated by Django 4.2.2 on 2023-07-25 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0004_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'verbose_name': '5. Class'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': '3. Section'},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'verbose_name': '2. Section'},
        ),
        migrations.AlterModelOptions(
            name='version',
            options={'verbose_name': '1. Versions'},
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Subject Code')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Subject Type')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Subject Name')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='subject_img/')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '4. Subject',
                'db_table': 'ac_subject',
            },
        ),
    ]