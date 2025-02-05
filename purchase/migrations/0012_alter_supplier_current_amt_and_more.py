# Generated by Django 4.2.2 on 2024-11-13 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0011_goodsreceiptnotemaster_confirm_with_pay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='current_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Current Balance'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='opening_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Opening Balance'),
        ),
    ]
