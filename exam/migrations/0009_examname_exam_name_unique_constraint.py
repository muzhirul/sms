# Generated by Django 4.2.2 on 2025-01-05 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_examroutinemst_examroutinedtl'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='examname',
            constraint=models.UniqueConstraint(fields=('name', 'status', 'institution', 'branch'), name='exam_name_unique_constraint'),
        ),
    ]
