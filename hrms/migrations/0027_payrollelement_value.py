# Generated by Django 4.2.2 on 2024-08-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0026_remove_payrollelement_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollelement',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
