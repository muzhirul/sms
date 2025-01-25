# Generated by Django 4.2.2 on 2025-01-06 11:24

import academic.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0264_alter_classsubject_book_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classsubject',
            name='book_file',
            field=academic.models.PDFFileField(blank=True, null=True, upload_to='book_file/', validators=[academic.models.validate_pdf_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Book File'),
        ),
        migrations.AddConstraint(
            model_name='version',
            constraint=models.UniqueConstraint(fields=('version', 'status', 'institution', 'branch'), name='unique_version_constraint'),
        ),
    ]
