# Generated by Django 4.2.2 on 2023-07-23 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
        ('admission', '0006_admission_created_by_admission_updated_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='Institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name'),
        ),
        migrations.AddField(
            model_name='guardian',
            name='relation',
            field=models.CharField(blank=True, choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('BROTHER', 'Brother'), ('SISTER', 'Sister')], max_length=20, null=True),
        ),
    ]
