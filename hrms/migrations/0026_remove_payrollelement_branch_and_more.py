# Generated by Django 4.2.2 on 2024-08-12 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0025_alter_payrollelement_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payrollelement',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='payrollelement',
            name='institution',
        ),
    ]
