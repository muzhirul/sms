# Generated by Django 4.2.2 on 2024-12-03 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0037_alter_guardian_mobile_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentenroll',
            name='admission_paid',
            field=models.CharField(default='Unpaid', max_length=10),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='mobile_no',
            field=models.CharField(blank=True, help_text='Enter a valid Bangladeshi mobile number (e.g., +8801712XXXXXX or 01712XXXXXX).', max_length=14, null=True, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='Invalid Bangladeshi mobile number format.', regex='^(?:\\+8801[3-9][0-9]{8}|01[3-9][0-9]{8})$')], verbose_name='Mobile No'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mobile_no',
            field=models.CharField(blank=True, help_text='Enter a valid Bangladeshi mobile number (e.g., +8801712XXXXXX or 01712XXXXXX).', max_length=14, null=True, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='Invalid Bangladeshi mobile number format.', regex='^(?:\\+8801[3-9][0-9]{8}|01[3-9][0-9]{8})$')], verbose_name='Mobile No'),
        ),
    ]
