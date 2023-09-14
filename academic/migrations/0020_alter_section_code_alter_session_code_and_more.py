# Generated by Django 4.2.2 on 2023-09-14 09:41

import academic.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0019_classsubject_image_remove_classsubject_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='code',
            field=models.CharField(blank=True, default=academic.models.generate_unique_code, max_length=20, null=True, unique=True, verbose_name='Section Code'),
        ),
        migrations.AlterField(
            model_name='session',
            name='code',
            field=models.CharField(blank=True, default=academic.models.generate_unique_code, max_length=20, null=True, unique=True, verbose_name='Session Code'),
        ),
        migrations.AlterField(
            model_name='version',
            name='code',
            field=models.CharField(blank=True, default=academic.models.generate_unique_code, max_length=20, null=True, unique=True, verbose_name='Version Code'),
        ),
    ]
