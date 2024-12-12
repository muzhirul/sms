# Generated by Django 4.2.2 on 2024-12-07 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0065_processstaffsalarytable_accounting'),
        ('student', '0038_studentenroll_admission_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentenroll',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staffshift'),
        ),
    ]