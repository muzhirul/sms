# Generated by Django 4.2.2 on 2025-01-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='punch_link',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Punch Device Link'),
        ),
    ]
