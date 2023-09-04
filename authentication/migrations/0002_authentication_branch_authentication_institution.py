# Generated by Django 4.2.2 on 2023-09-04 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authentication',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch'),
        ),
        migrations.AddField(
            model_name='authentication',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution'),
        ),
    ]
