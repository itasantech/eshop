# Generated by Django 4.1.6 on 2023-02-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0008_customer_city_ar_customer_name_ar_product_title_ar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city_en',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='customer',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='city_en',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='full_name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='full_name'),
        ),
    ]
