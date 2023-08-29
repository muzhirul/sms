# Generated by Django 4.2.2 on 2023-08-06 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='parent',
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Branch Code')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Branch Name')),
                ('mobile_no', models.CharField(blank=True, max_length=11, null=True, verbose_name='Mobile No')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email Address')),
                ('short_address', models.TextField(blank=True, null=True, verbose_name='Short Address')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('map_link', models.URLField(blank=True, max_length=255, null=True, verbose_name='Map Address')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ins_branch',
            },
        ),
    ]