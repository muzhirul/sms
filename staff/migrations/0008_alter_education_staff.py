# Generated by Django 4.2.2 on 2023-10-09 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_alter_staff_blood_group_alter_staff_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_education', to='staff.staff'),
        ),
    ]
