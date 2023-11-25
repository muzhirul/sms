# Generated by Django 4.2.2 on 2023-11-25 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0037_day_week_end'),
        ('staff', '0017_rename_institution_staff_institution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='board',
        ),
        migrations.AddField(
            model_name='education',
            name='edu_board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.educationboard'),
        ),
    ]
