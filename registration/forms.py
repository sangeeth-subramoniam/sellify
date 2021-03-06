from django import forms
from django.contrib.auth.models import User
from .models import user_profile

class User_form(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("username", "email" , "password")


class user_profile_form(forms.ModelForm):
    
    class Meta:
        model = user_profile
        fields = ("phone", "age" , "address", "profile_picture", "bio")


class user_profile_update_form(forms.ModelForm):

    class Meta:
        model = user_profile
        fields = ["address","bio"]

    
class user_profile_picture_update_form(forms.ModelForm):

    class Meta:
        model = user_profile
        fields = ["profile_picture" , ]