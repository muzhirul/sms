# Generated by Django 4.2.2 on 2024-01-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0015_remove_holiday_is_general_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
