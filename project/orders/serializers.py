from rest_framework import serializers
from .models import *


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

class Products_SoldSerializers(serializers.ModelSerializer):

    class Meta:
        model = Products_Sold
        fields = "__all__"