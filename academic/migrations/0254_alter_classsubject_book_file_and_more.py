# Generated by Django 4.2.2 on 2024-10-31 09:48

import academic.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0253_alter_classsubject_book_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classsubject',
            name='book_file',
            field=academic.models.PDFFileField(blank=True, null=True, upload_to='book_file/', validators=[academic.models.validate_pdf_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Book File'),
        ),
        migrations.AddConstraint(
            model_name='classroutiinedtl',
            constraint=models.UniqueConstraint(fields=('day', 'teacher', 'status', 'institution', 'branch'), name='unique_class_routine_dtl_constraint'),
        ),
    ]
