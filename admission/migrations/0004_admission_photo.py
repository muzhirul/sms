# Generated by Django 4.2.2 on 2023-07-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0003_admission_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='admission_photo/', verbose_name='Photo'),
        ),
    ]
