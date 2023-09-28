# Generated by Django 4.2.2 on 2023-09-20 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0010_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_create', models.BooleanField(default=False)),
                ('can_view', models.BooleanField(default=False)),
                ('can_update', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=False)),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup_app.menu')),
            ],
            options={
                'db_table': 's_permission',
            },
        ),
    ]