# Generated by Django 3.2.9 on 2021-12-08 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_shop_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop_products',
            name='category',
        ),
        migrations.AddField(
            model_name='shop_products',
            name='category',
            field=models.ManyToManyField(related_name='product_cat', to='product.shop_categories'),
        ),
    ]
