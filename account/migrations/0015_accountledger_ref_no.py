# Generated by Django 4.2.2 on 2024-10-02 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_chartofaccounts_fin_stat_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountledger',
            name='ref_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
