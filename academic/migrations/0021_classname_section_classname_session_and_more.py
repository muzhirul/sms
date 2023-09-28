# Generated by Django 4.2.2 on 2023-09-18 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0020_alter_section_code_alter_session_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classname',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.section'),
        ),
        migrations.AddField(
            model_name='classname',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.session'),
        ),
        migrations.AddField(
            model_name='classname',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.version'),
        ),
    ]