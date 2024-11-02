# Generated by Django 4.2.2 on 2024-11-02 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_branch_institution'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_alter_warehouse_category_brand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Category Name')),
                ('keyword', models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='Keyword')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.branch')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_creator', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.institution', verbose_name='Institution Name')),
                ('updated_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_update_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'db_table': 'inv_category',
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name', 'keyword', 'status', 'institution', 'branch'), name='category_unique_constraint'),
        ),
    ]
