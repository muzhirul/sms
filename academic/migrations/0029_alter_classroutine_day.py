# Generated by Django 4.2.2 on 2023-10-14 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0017_day_sl_no'),
        ('academic', '0028_alter_classroutine_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroutine',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup_app.day', verbose_name='Day'),
        ),
    ]
