from datetime import datetime, timedelta
from django.shortcuts import render , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AccountSerializers , SigninSerializers
from .models import Profile
# Create your views here.


@api_view(['POST'])
def creatuser(request):

    data = request.data
    user = AccountSerializers(data=data)

    if user.is_valid():
        if not User.objects.filter(email = data['email']).exists():
            User.objects.create(
                username = data['username'],
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = make_password(data['password']),
            )
            return Response({
                'Response': 'Your Account Register Successfuly'
            },
            status= status.HTTP_201_CREATED
            )
        else:
            return Response({
                'Errors': 'Your Account Is Already Registed'
            },
            status= status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = SigninSerializers(request.user)

    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_account(request):
    data = request.data

    request.user.first_name = data['first_name']
    request.user.last_name  = data['last_name']
    request.user.email      = data['email']
    request.user.save()

    serializer = AccountSerializers(request.user , many = False)

    return Response(serializer.data)


def get_current_host(request):
    protocol = request.is_secure() or 'https' or 'http'
    host = request.get_host()

    return f'{protocol}://{host}/'


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User , email = data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = f'{host}/api/reset_password/{token}'
    body = f'Your password reset link is : {link}'

    send_mail(
        "Paswword reset from eMarket",
        body,
        'Omar.ahmed01067@gmail.com',
        [data['email']]
    )
    
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_password(request , token):
    data = request.data
    user = get_object_or_404(User , profile__reset_password_token= token)

    # if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
    #     return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    else:
        user.password = make_password(data['password'])
        user.profile.reset_password_token = ''
        user.profile.reset_password_expire = None

        user.profile.save() 
        user.save()

        return Response({'details': 'Password reset done '})

    