# Generated by Django 4.2.2 on 2023-11-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0021_staffpayroll_contract_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffpayroll',
            name='remarks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]