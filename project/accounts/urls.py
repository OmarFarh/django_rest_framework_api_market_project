from django.urls import path
from . import views

urlpatterns = [
    path('create' , views.creatuser , name='Create_User'),
    path('info' , views.current_user , name='Info'),
    path('update' , views.update_account , name='Update'),
    path('forget_password' , views.forgot_password , name='Foget_password'),
    path('reset_password/<str:token>' , views.reset_password , name='Reset_password'),
]