# Generated by Django 4.2.2 on 2023-07-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-')], max_length=5, null=True, verbose_name='Blood Group'),
        ),
        migrations.AddField(
            model_name='admission',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admission',
            name='permanent_address',
            field=models.TextField(blank=True, null=True, verbose_name='Permanent Address'),
        ),
        migrations.AddField(
            model_name='admission',
            name='present_address',
            field=models.TextField(blank=True, null=True, verbose_name='Present Address'),
        ),
        migrations.AddField(
            model_name='admission',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='admission',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='admission',
            name='admission_no',
            field=models.CharField(blank=True, editable=False, max_length=15, null=True, verbose_name='Admission No'),
        ),
    ]
