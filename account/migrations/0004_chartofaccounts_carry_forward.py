# Generated by Django 4.2.2 on 2024-09-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_chartofaccounts_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartofaccounts',
            name='carry_forward',
            field=models.BooleanField(default=False),
        ),
    ]
