from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User

# Create your models here.

ADMIN_USER_ID = 1

class shop_categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return str( str(self.category_name).capitalize())

class shop_products(models.Model):

    id = models.AutoField(primary_key=True)
    shop_product_name = models.CharField(max_length=100, default = "Unnamed", blank=True, null=True)
    shop_product_desc = models.CharField(max_length=500, default= " No Description Available! ", blank=True, null=True)
    shop_product_cost = models.IntegerField(blank=True, null=True)
    category = models.ManyToManyField(shop_categories, related_name="product_cat")
    created_at = models.DateTimeField(null=True , auto_now_add=True)

    created_by = models.ForeignKey(User, default = ADMIN_USER_ID, on_delete=models.CASCADE)

    shop_product_image = ResizedImageField(size=[370, 530], upload_to="shop_product_images", default = "default_shop_product", blank=True, null=True)
    shop_product_image2 = ResizedImageField(size=[370, 530], upload_to="shop_product_images",  blank=True, null=True)
    shop_product_image3 = ResizedImageField(size=[370, 530], upload_to="shop_product_images",  blank=True, null=True)
    shop_product_image4 = ResizedImageField(size=[370, 530], upload_to="shop_product_images",  blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.id) + str(' ') + str(self.shop_product_name)


class reviews(models.Model):
    
    id = models.AutoField(primary_key=True)
    reviewed_pdt = models.ForeignKey(shop_products, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=7)
    review = models.CharField(max_length=900)
    created_on = models.DateTimeField()

    def __Str__(self):
        return str(self.id) + str(self.reviewed_pdt.shop_product_name)

