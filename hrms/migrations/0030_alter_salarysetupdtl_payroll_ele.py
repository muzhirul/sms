# Generated by Django 4.2.2 on 2024-08-20 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0029_salarysetupdtl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarysetupdtl',
            name='payroll_ele',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': 'True'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms.payrollelement', verbose_name='Element'),
        ),
    ]