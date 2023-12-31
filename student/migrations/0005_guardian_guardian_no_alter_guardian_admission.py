# Generated by Django 4.2.2 on 2023-09-14 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_student_student_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='guardian_no',
            field=models.CharField(blank=True, editable=False, max_length=15, null=True, verbose_name='Guardian No'),
        ),
        migrations.AlterField(
            model_name='guardian',
            name='admission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_guardian', to='student.student'),
        ),
    ]
