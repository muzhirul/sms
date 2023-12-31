# Generated by Django 4.2.2 on 2023-12-07 09:35

import academic.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_branch_institution'),
        ('staff', '0031_staff_doj'),
        ('academic', '0123_alter_classsubject_book_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classsubject',
            name='book_file',
            field=academic.models.PDFFileField(blank=True, null=True, upload_to='book_file/', validators=[academic.models.validate_pdf_file_size, django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Book File'),
        ),
        migrations.CreateModel(
            name='ClassTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.branch')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classname', verbose_name='Class Name')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher_creator', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.classgroup')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institution.institution')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.section', verbose_name='Section')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.session', verbose_name='Session')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff', verbose_name='Teacher Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher_update_by', to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.version', verbose_name='Version')),
            ],
            options={
                'db_table': 'ac_class_teacher',
            },
        ),
    ]
