from django.urls import path
from . import views

urlpatterns = [
    path('' , views.products , name= 'Products'),
    path('<int:id>/' , views.product_details , name= 'Details'),
    path('new/' , views.new_product , name= 'New_Broduct'),
    path('update/<int:id>' , views.update_product , name= 'Update_Product'),
    path('delete/<int:id>' , views.delete_product , name= 'Delete_Product'),
    path('review/<int:id>' , views.create_reviwe , name= 'Add_Review'),
    path('delete_rev/<int:id>' , views.delete_review , name= 'Delete_Review'),
]