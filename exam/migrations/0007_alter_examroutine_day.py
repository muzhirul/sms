# Generated by Django 4.2.2 on 2023-10-19 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_alter_examroutine_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examroutine',
            name='day',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Exam Day'),
        ),
    ]
