import django_filters 
from .models import Transaction
from django import forms

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta: 
        model = Transaction
        fields = ['category',]

  
        

        