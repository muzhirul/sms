# Generated by Django 4.2.2 on 2024-01-30 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0050_holidaytype'),
        ('hrms', '0018_holiday_end_time_holiday_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='holiday_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.holidaytype', verbose_name='Holiday Type'),
        ),
    ]
