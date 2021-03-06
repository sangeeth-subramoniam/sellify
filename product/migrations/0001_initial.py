# Generated by Django 3.2.9 on 2021-12-07 06:05

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='shop_products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_product_name', models.CharField(blank=True, default='Unnamed', max_length=100, null=True)),
                ('shop_product_desc', models.CharField(blank=True, default=' No Description Available! ', max_length=500, null=True)),
                ('shop_product_cost', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=600, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('shop_product_image', django_resized.forms.ResizedImageField(blank=True, crop=None, default='default_shop_product', force_format='JPEG', keep_meta=True, null=True, quality=100, size=[370, 530], upload_to='shop_product_images')),
            ],
        ),
    ]
