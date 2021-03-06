# Generated by Django 3.2.9 on 2021-12-16 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0007_shop_products_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.CharField(max_length=900)),
                ('created_on', models.DateTimeField()),
                ('reviewed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reviewed_pdt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.shop_products')),
            ],
        ),
    ]
