# Generated by Django 4.2.2 on 2024-08-31 12:11

from django.db import migrations, models
import hrms.models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0035_accounttaxmst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttaxmst',
            name='code',
            field=models.CharField(default=hrms.models.acc_tax_mst_code, editable=False, max_length=20),
        ),
    ]
