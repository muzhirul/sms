# Generated by Django 4.2.2 on 2023-10-16 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0033_alter_classroom_floor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='classsection',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.version'),
        ),
    ]