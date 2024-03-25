from django.shortcuts import render , get_object_or_404
from .models import *
from .serializers import OrderSerializers , Products_SoldSerializers

from rest_framework.response import Response
from rest_framework.decorators import permission_classes , api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from products.models import Product
from datetime import datetime
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_card(request , id):

    data = request.data
    product = get_object_or_404(Product , id = id)
    user = request.user

    if Order.objects.filter(user = user , is_finshed = False).exists():
        
        if Products_Sold.objects.filter(order__is_finshed = False , order__user = user , id = id).exists():
            my_order = Products_Sold.objects.get(order__is_finshed = False , order__user = user , id = id)
            my_order.items_count = data['items_count']
            my_order.total_price = float(product.price) * float(data['items_count'])
            my_order.save()

        else:
            Products_Sold.objects.create(
                order = Order.objects.get(user = user , is_finshed = False),
                product = product,
                items_count = data['items_count'],
                total_price = float(product.price) * float(data['items_count'])
            )

    else:
        Order.objects.create(
            user = user,
            countery = data['countery'],
            city = data['city'],
            address = data['address'],
            time = datetime.now(),
        )
        Products_Sold.objects.create(
            order = Order.objects.get(user = user , is_finshed = False),
            product = product,
            items_count = data['items_count'],
            total_price = float(product.price) * float(data['items_count'])
        )

    return Response({'Success': 'The product has been successfully added to the shopping cart'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):

    user = request.user
    products = Products_Sold.objects.filter(order__user = user , order__is_finshed = False)

    # response = Products_SoldSerializers(products , many = True)

    pagenator = PageNumberPagination()
    pagenator.page_size = 2
    queryset = pagenator.paginate_queryset(products , request)

    response = Products_SoldSerializers(queryset , many = True)

    if products.exists():
        return Response({'Shopping cart': response.data})
    else:
        return Response({'Shopping cart': 'Your shopping cart is empty'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request , id):

    product = get_object_or_404(Products_Sold , id = id)
    user = request.user

    if product.order.user == user:
        product.delete()

        return Response({'Delete': 'The product has been successfully deleted'})
    else:
        return Response({'Error': 'Wrong product'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirm_order(request):
    
    user = request.user
    order = get_object_or_404(Order , user = user , is_finshed = False)
    products = Products_Sold.objects.filter(order = order)

    if products.exists():
        sum = 0
        for i in products:
            sum += float(i.total_price)

        order.is_finshed = True
        order.total_price = sum
        order.save()

        return Response({'Success': 'Your purchase has been confirmed successfully'})
    else:
        return Response({'Shopping cart': 'Your shopping cart is empty'})
