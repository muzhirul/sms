# Generated by Django 4.2.2 on 2023-08-06 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0015_classsection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='version',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Version'),
        ),
    ]
