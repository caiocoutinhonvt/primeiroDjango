from django.contrib import admin
from .models import Category, Transaction, Profile

# Register your models here.

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Profile)
