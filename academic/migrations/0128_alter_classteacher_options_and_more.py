# Generated by Django 4.2.2 on 2023-12-10 10:38

import academic.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_app', '0042_attendancetype'),
        ('academic', '0127_alter_classsubject_book_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classteacher',
            options={'verbose_name': 'Assign Class Teacher'},
        ),
        migrations.RemoveField(
            model_name='classroutinemst',
            name='day',
        ),
        migrations.AddField(
            model_name='classroutiinedtl',
            name='day',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='setup_app.days', verbose_name='Day'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classsubject',
            name='book_file',
            field=academic.models.PDFFileField(blank=True, null=True, upload_to='book_file/', validators=[academic.models.validate_pdf_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Book File'),
        ),
    ]
