# Generated by Django 4.2.2 on 2023-09-20 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0013_bloodgroup_status_gender_status_menu_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.role'),
        ),
    ]
