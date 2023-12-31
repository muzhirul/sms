# Generated by Django 4.2.2 on 2023-10-11 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0015_alter_permission_can_view'),
        ('staff', '0013_alter_staffshift_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_gender', to='setup_app.religion'),
        ),
    ]
