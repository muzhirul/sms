# Generated by Django 4.2.2 on 2023-10-30 10:54

import academic.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0042_alter_classsubject_book_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classsubject',
            name='book_file',
            field=academic.models.PDFFileField(blank=True, null=True, upload_to='book_file/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Book File'),
        ),
    ]
