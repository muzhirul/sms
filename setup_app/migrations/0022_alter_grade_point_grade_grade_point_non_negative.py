# Generated by Django 4.2.2 on 2023-10-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0021_alter_grade_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='point',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Grade Point'),
        ),
        migrations.AddConstraint(
            model_name='grade',
            constraint=models.CheckConstraint(check=models.Q(('point__gte', 0)), name='grade_point_non_negative'),
        ),
    ]
