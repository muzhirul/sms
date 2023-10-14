# Generated by Django 4.2.2 on 2023-10-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0018_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.CharField(max_length=5, verbose_name='Grade Name'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='point',
            field=models.IntegerField(verbose_name='Grade Point'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='sl_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
