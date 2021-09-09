from django.contrib import admin
from django.db import models
from .models import Category, Product, FeedBack, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    fieldsets = [
        (
            None, {
                'fields':('name',)
            }
        )
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'status','price', 'image', 'created', 'updated', 'active', 'author']
    list_filter = ['category', 'status']


@admin.register(FeedBack)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['text', 'product', 'user']
    search_fields = ['text', 'product__name', 'product__description']



admin.site.register(Cart)

class CartItemAdmin(admin.ModelAdmin):
    list_display =['product']

admin.site.register(CartItem, CartItemAdmin)

    
