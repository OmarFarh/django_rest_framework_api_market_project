from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User , related_name='profile' ,on_delete = models.CASCADE)
    reset_password_token = models.CharField(max_length = 50 , null = True , blank = True, )
    reset_password_expire = models.DateField(null = True , blank = True)



def createprofile(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user = kwargs['instance'])

post_save.connect(createprofile , sender= User)
    
