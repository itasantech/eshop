# Generated by Django 4.1.6 on 2023-02-24 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0007_remove_customer_city_en_remove_customer_name_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city_ar',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='customer',
            name='name_ar',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_ar',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='city_ar',
            field=models.TextField(null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='salesman',
            name='full_name_ar',
            field=models.CharField(max_length=100, null=True, verbose_name='full_name'),
        ),
    ]
