# Generated by Django 4.2.2 on 2023-12-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0042_alter_processattendancedaily_early_gone_by_min_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processattendancedaily',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Duraion'),
        ),
    ]
