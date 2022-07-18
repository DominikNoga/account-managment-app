import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    category = CharFilter(field_name="product__category", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ["status"]