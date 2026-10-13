from django import forms
from .models import Profile
from django.db import models
from django.contrib.auth.models import User

class UserRegisterform(forms.Form):
    username = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder':'enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'enter your email'}))
    first_name = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder':'enter you first name'}))
    last_name = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder':'enter you last name'}))
    password1 = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"placeholder":"enter your password"}))
    password2 = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"placeholder":"enter your password again"}))

    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError("username already exist")
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email alredy exist")
        else:
            return email
        
    def clean_password2(self):
        password_1 = self.cleaned_data['password1']
        password_2 = self.cleaned_data['password2']
        if password_1 != password_2:
            raise forms.ValidationError("second pass ia not the same , try again")
        elif len(password_2) < 8 :
            raise forms.ValidationError("pass should be more than 8 character, try again")
        elif not any (x.isupper()for x in password_2):
             raise forms.ValidationError("there should be upper character one")
        return password_2
    
class UserLoginform(forms.Form):
    username = forms.CharField(max_length =40)
    password = forms.CharField(max_length =40)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ['phone','address']
