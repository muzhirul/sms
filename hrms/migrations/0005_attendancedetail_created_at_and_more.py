# Generated by Django 4.2.2 on 2023-11-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0004_attendancedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancedetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancedetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
