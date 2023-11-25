# Generated by Django 4.2.2 on 2023-11-25 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0085_alter_classgroup_code_alter_classsubject_book_file'),
        ('student', '0018_student_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentenroll',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.classgroup'),
        ),
    ]
