# Generated by Django 4.2.2 on 2024-05-14 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0209_alter_classsubject_book_file'),
        ('setup_app', '0051_paymentmethod'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('communicate', '0003_smstemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsSendSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('send_option', models.CharField(max_length=10, verbose_name='Send Through')),
                ('message_body', models.TextField(verbose_name='Message')),
                ('send_datetime', models.DateTimeField(blank=True, null=True)),
                ('is_process', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('class_section', models.ManyToManyField(to='academic.classsection')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sms_setup_creator', to=settings.AUTH_USER_MODEL)),
                ('group', models.ManyToManyField(to='setup_app.role')),
                ('individual', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communicate.smstemplate', verbose_name='SMS Template')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sms_setup_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Send SMS',
                'db_table': 'comm_sms_send_setup',
            },
        ),
    ]
