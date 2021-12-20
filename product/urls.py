from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'
urlpatterns = [
    path('', views.shop , name = "shop"),
    path('productdetail/<int:pk>', views.shop_product_detail , name = "shop_product_detail"),
    path('shop_product_category/<pk>', views.shop_product_category , name = "shop_product_category"),
    path('productsell/', views.sell , name = "sell"),
    path('add_to_cart/<int:pk>', views.add_to_cart , name = "add_to_cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
