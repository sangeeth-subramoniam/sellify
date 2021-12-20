from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'homepage'
urlpatterns = [
    path('', views.home , name = "home"),
    path('categories/', views.categories , name = "categories"),
    path('about/', views.about , name = "about"),
    path('index/', views.index , name = "index"),
    path('about/', views.about , name = "about"),
    path('contactus/', views.contactus , name = "contactus"),
    path('singleproduct/', views.singleproduct , name = "singleproduct"),
    path('subscribe/', views.subscription , name = "subscription"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
