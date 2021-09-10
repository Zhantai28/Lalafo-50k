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



class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'image', 'status','price', 'created', 'updated', 'active', 'author']
    list_filter = ['category', 'status']
admin.site.register(Product)



@admin.register(FeedBack)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['text', 'product', 'user', 'created', 'updated', 'active']
    search_fields = ['text', 'product__name', 'product__description']
    list_filter = ['product', 'active', 'created']




admin.site.register(Cart)

class CartItemAdmin(admin.ModelAdmin):
    list_display =['product']

admin.site.register(CartItem, CartItemAdmin)

    
