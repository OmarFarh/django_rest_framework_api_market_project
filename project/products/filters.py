import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    minprice = django_filters.CharFilter(field_name= 'price' , lookup_expr = 'gte')
    maxprice = django_filters.CharFilter(field_name= 'price' , lookup_expr = 'lte')

    class Meta:
        model = Product
        fields = ['name', 'minprice' , 'maxprice']