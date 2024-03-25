from django.shortcuts import render , get_object_or_404
from .serializers import ProductSerializers
from .models import Product , Review
from django.contrib.auth.models import User

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .filters import ProductFilter
# Create your views here.

@api_view(['GET'])
def products(request):
    
    products = Product.objects.all()
    filter = ProductFilter(request.GET , queryset= products.order_by('-id'))

    paginator = PageNumberPagination()
    paginator.page_size = 2
    queryset = paginator.paginate_queryset(filter.qs , request)

    res = ProductSerializers(queryset, many= True)

    return Response(res.data)


@api_view(['GET'])
def product_details(request , id):

    product = Product.objects.get(id = id)
    res = ProductSerializers(product , many = False)

    return Response(res.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serlizer = ProductSerializers(data=data)

    if serlizer.is_valid():
        product = Product.objects.create(**data , user = request.user)
        response = ProductSerializers(product , many = False)

        return Response({"Product":response.data})
    else:
        return Response(serlizer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request , id):
    data = request.data
    product = get_object_or_404(Product , id = id)

    if request.user != product.user:
        return Response({'Error': 'This product belongs to another user'},
                        status= status.HTTP_403_FORBIDDEN)
    else:
        product.name = data['name']
        product.price = data['price']
        product.description = data['description']
        product.is_active = data['is_active']
        product.save()

        serializer = ProductSerializers(product , many = False)

        return Response(serializer.data)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request , id):
    product = get_object_or_404(Product , id = id)

    if request.user != product.user:
        return Response({'Error': 'This product belongs to another user'},status= status.HTTP_403_FORBIDDEN)
    else:
        product.delete()
        return Response({'Delete': 'Success Deleted Process'} , status= status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reviwe(request , id):

    product = get_object_or_404(Product , id = id)
    user = request.user
    data = request.data
    review = Review.objects.all()

    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({'error':'please select between 1 to 5'})
    
    elif review.filter(user = user , product = product).exists():
        new_review = Review.objects.get(user = user , product = product)
        new_review.rating = data['rating']
        new_review.comment = data['comment']
        new_review.save()

        # count_rev = review.filter(product = product).count()
        review_avg = float(product.reviwes) + float(data['rating'])

        product.reviwes = review_avg - new_review.rating
        product.save()
        return Response({'Success': 'Your Coment Is Updated'})
    
    else:
        Review.objects.create(
            product = product,
            user = user,
            rating = data['rating'],
            comment = data['comment'],
        )

        # count_rev = review.filter(product = product).count()
        review_avg = float(product.reviwes) + float(data['rating'])

        product.reviwes = review_avg
        product.save()

        return Response({'Success': 'Your Coment Is added'})
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request , id):

    user = request.user

    if Review.objects.filter(id=id).exists():
        review = Review.objects.get(id = id) 

        if not review.user == user :
            return Response({'error': 'Not Found The Comment'})
        
        elif review.user == user :
            review.delete()
            return Response({'Success': 'Your review is deleted'})
    
    else:
        return Response({'error': 'we not found any review'} , status= status.HTTP_400_BAD_REQUEST)
    
