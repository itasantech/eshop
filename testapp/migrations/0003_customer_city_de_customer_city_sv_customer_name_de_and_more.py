# Generated by Django 4.1.6 on 2023-02-24 00:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_alter_order_salesmen_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city_de',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='customer',
            name='city_sv',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='customer',
            name='name_de',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='customer',
            name='name_sv',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_de',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_sv',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='city_de',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='city_sv',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='full_name_de',
            field=models.CharField(max_length=100, null=True, verbose_name='full_name'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='full_name_sv',
            field=models.CharField(max_length=100, null=True, verbose_name='full_name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.TextField(verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='grade',
            field=models.IntegerField(verbose_name='grade'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.date.today, verbose_name='order_date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='order_id'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='total_price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='salesman',
            name='city',
            field=models.TextField(verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='salesman',
            name='commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='commission'),
        ),
        migrations.AlterField(
            model_name='salesman',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='full_name'),
        ),
    ]