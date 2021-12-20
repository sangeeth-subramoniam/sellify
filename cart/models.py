from django.db import models

from product.models import shop_products
from django.contrib.auth.models import User

# Create your models here.
class cart(models.Model):
    id = models.AutoField(primary_key=True)

    cart_product = models.ForeignKey(shop_products, on_delete=models.CASCADE)
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(blank = True, null=True)
    cart_status = models.TextField(max_length=7, default="pending")

    def __str__(self):
        return str(self.id) + str(self.cart_user.username) + str(self.cart_product.shop_product_name)

class order(models.Model):
    id = models.AutoField(primary_key=True)
    order_products = models.ManyToManyField(shop_products, related_name="order_pdts")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank = True, null=True)
    order_status = models.CharField(max_length=7, default = "pending")
    order_cost = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return str(self.created_by) + str(self.id)





