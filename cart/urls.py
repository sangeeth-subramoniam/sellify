from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'cart'
urlpatterns = [
    path('', views.cart_home , name = "cart_home"),
    path('place_order', views.place_order , name = "place_order"),
    path('view_orders', views.view_orders , name = "view_orders"),
    path('orderplaced', views.orderplaced , name = "orderplaced"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
