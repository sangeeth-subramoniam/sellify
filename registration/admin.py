from django.contrib import admin
from .models import user_profile, logs
# Register your models here.

admin.site.register(user_profile)
admin.site.register(logs)


