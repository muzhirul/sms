# Generated by Django 4.2.2 on 2024-09-19 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartofaccounts',
            name='income_stat_type',
            field=models.CharField(blank=True, choices=[('Operating', 'Operating'), ('Financial', 'Financial')], max_length=50, null=True, verbose_name='Income Statement Type'),
        ),
    ]
