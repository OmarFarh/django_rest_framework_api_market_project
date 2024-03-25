from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.



class Order(models.Model):

    user = models.ForeignKey(User , on_delete = models.CASCADE)
    countery = models.CharField(max_length = 50) 
    city = models.CharField(max_length = 50)
    address = models.CharField(max_length = 100)
    time = models.DateTimeField()
    total_price = models.DecimalField(max_digits = 7 , decimal_places= 2 , null = True , blank = True)
    is_finshed = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.user.username


class Products_Sold(models.Model):

    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    items_count = models.IntegerField()
    total_price = models.DecimalField(max_digits = 7 , decimal_places= 2)

    def __str__(self) -> str:
        return self.product.name
