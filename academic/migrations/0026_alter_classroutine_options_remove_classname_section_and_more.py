# Generated by Django 4.2.2 on 2023-10-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0025_classroutine'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroutine',
            options={'verbose_name': 'Class Routine'},
        ),
        migrations.RemoveField(
            model_name='classname',
            name='section',
        ),
        migrations.RemoveField(
            model_name='classname',
            name='session',
        ),
        migrations.RemoveField(
            model_name='classname',
            name='version',
        ),
    ]
