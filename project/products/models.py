from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):

    user = models.ForeignKey(User , on_delete= models.CASCADE , blank = True , null = True)
    name = models.CharField(max_length = 50)
    description = models.TextField()
    price = models.DecimalField(max_digits = 7 , decimal_places= 2 )
    is_active = models.BooleanField(default = True)
    reviwes = models.DecimalField(max_digits = 7 , decimal_places= 2 , default = 0 , null=True)
    time = models.DateField(auto_now = True)

    def __str__(self) -> str:
        return self.name


class Review (models.Model):

    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)
    comment = models.TextField(default = '')

    def __str__(self) -> str:
        return self.comment