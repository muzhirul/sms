# Generated by Django 4.2.2 on 2024-11-26 16:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0035_alter_student_mobile_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardian',
            name='mobile_no',
            field=models.CharField(blank=True, help_text='Enter a valid Bangladeshi mobile number (e.g., +8801712345678 or 01712345678).', max_length=11, null=True, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='Invalid Bangladeshi mobile number format.', regex='^(?:\\+8801[3-9][0-9]{8}|01[3-9][0-9]{8})$')], verbose_name='Mobile No'),
        ),
    ]
