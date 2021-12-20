from django.db import models
from django.contrib.auth.models import User

from django.core.validators import  MinValueValidator,MaxValueValidator

# Create your models here.

class user_profile(models.Model):

    #using default User model by linking 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional fields
    phone = models.CharField(max_length=11)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    address = models.CharField(max_length=200)

    profile_picture = models.ImageField(upload_to='profile_pictures' , blank = True )
    bio = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.user.username