# Generated by Django 4.2.2 on 2024-09-29 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0012_alter_feesdetails_fix_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedetailsbreakdown',
            name='fees_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_break_down', to='fees.feesdetails'),
        ),
    ]
