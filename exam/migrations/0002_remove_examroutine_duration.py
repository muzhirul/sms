# Generated by Django 4.2.2 on 2023-10-18 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examroutine',
            name='duration',
        ),
    ]