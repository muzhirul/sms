# Generated by Django 4.2.2 on 2024-02-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_authentication_role_authentication_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='authentication',
            name='model_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
