# Generated by Django 4.1.6 on 2023-02-24 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_customer_city_en_customer_name_en_product_title_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='city_en',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='salesman',
            name='city_en',
        ),
        migrations.RemoveField(
            model_name='salesman',
            name='full_name_en',
        ),
    ]
