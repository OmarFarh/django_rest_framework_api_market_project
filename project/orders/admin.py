from django.contrib import admin
from .models import *
# Register your models here.


class Order_details(admin.ModelAdmin):

    list_display = ['user' , 'id' , 'time']


admin.site.register(Order , Order_details)
admin.site.register(Products_Sold)