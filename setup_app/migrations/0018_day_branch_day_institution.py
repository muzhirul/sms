# Generated by Django 4.2.2 on 2023-10-14 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        ('setup_app', '0017_day_sl_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch', verbose_name='Branch Name'),
        ),
        migrations.AddField(
            model_name='day',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name'),
        ),
    ]
