from django.db import models
from django.db.models.fields import AutoField, EmailField
from django.http import request
from django.contrib.auth.models import User

# Create your models here.
class subscribe(models.Model):
    id = AutoField(primary_key=True)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = EmailField(max_length=50)
    created_on = models.DateTimeField()

    def __str__(self):
        return str(self.email) + str(self.name.username)