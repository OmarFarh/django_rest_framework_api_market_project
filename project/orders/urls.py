from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_orders , name= 'My_Order'),
    path('add/<int:id>' , views.add_to_card , name= 'Add_Card'),
    path('delete/<int:id>' , views.delete_item , name= 'Delete_item'),
    path('confirm_order' , views.confirm_order , name= 'Confirm_Order'),
]