# Generated by Django 4.2.2 on 2023-10-09 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_alter_staff_code_alter_staff_staff_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='Institution',
        ),
        migrations.RemoveField(
            model_name='education',
            name='branch',
        ),
    ]
