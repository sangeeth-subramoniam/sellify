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

class logs(models.Model):
    logid = models.AutoField(primary_key=True)
    logger = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=50 , blank=True , null = True)
    status = models.CharField(max_length=10 , blank=True , null= True)
    start_time = models.DateTimeField(blank=True , auto_created=True)
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True , null=True)

    def __str__(self):
        return str(str(self.logid) + str(self.logger))