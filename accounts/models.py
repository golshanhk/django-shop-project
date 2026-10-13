from django.db import models
from  phone_field import PhoneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete,pre_save,post_delete,m2m_changed


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(max_length=20,null=True,blank=True)
    address= models.TextField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.user.username

    def save_profile_user(sender,**kwargs):
        if kwargs['created']:
            profile_user=Profile(user = kwargs['instance'])
            profile_user.save()
    post_save.connect(save_profile_user,sender=User)