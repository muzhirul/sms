# Generated by Django 4.2.2 on 2023-07-25 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
        ('academic', '0006_version_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'verbose_name': '1. Version'},
        ),
        migrations.AddField(
            model_name='subject',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution'),
        ),
        migrations.AddField(
            model_name='subject',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='version',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='type',
            field=models.CharField(blank=True, choices=[('THEORY', 'Theory'), ('PARCTICAL', 'Practical')], max_length=20, null=True, verbose_name='Subject Type'),
        ),
    ]
