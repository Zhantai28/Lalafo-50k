from django.contrib import admin
from .models import Category, Product

# class AdminProduct(admin.ModelAdmin):
admin.site.register(Category)
admin.site.register(Product)

