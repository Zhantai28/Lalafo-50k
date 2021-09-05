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
    list_display = ['category', 'name', 'description', 'status','price', 'created', 'updated', 'active']
    list_filter = ['category', 'status']


@admin.register(FeedBack)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['text', 'product', 'user']
    search_fields = ['text', 'product__name', 'product__description']
    fields = ['user', 'product', 'text']
    readonly_fields = ['product', 'text']

admin.site.register(FeedBack, FeedbackAdmin) 
fieldsets = [
        (
            None, {
                'fields':('category', 'sub_category', 'name', 'slug','description', 'status', 'price'),
            
            },
        )
]

def product_count(self, obj):
    return obj.product_set.count()




admin.site.register(Cart)

class CartItemAdmin(admin.ModelAdmin):
    list_display =['product']

admin.site.register(CartItem, CartItemAdmin)

    
