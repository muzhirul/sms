# Generated by Django 4.2.2 on 2024-02-25 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0005_feesdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='feesdetails',
            name='fees_master',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fees.feesmaster'),
            preserve_default=False,
        ),
    ]