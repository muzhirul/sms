# Generated by Django 4.2.2 on 2023-12-23 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0041_alter_staffleavetransaction_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processattendancedaily',
            name='early_gone_by_min',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='processattendancedaily',
            name='late_by_min',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
