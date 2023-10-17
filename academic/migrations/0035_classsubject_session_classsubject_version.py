# Generated by Django 4.2.2 on 2023-10-16 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0034_classsection_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='classsubject',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.session'),
        ),
        migrations.AddField(
            model_name='classsubject',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.version'),
        ),
    ]