from django.contrib import admin
from .models import shop_products, shop_categories, reviews

# Register your models here.
admin.site.register(shop_categories)
admin.site.register(shop_products)
admin.site.register(reviews)
