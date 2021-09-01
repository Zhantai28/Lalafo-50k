from django.contrib import admin
from django.db import models
from .models import Category, Product, Subcategory

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fieldsets = [
        (
            None, {
                'fields':('name',)
            }
        )
    ]
    inlines = (SubcategoryInline,)

@admin.register(Subcategory)
class SubategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'sub_category', 'name', 'description', 'status', 'price', 'created', 'updated']
    list_filter = ['category', 'status']
    fieldsets = [
        (
            None, {
                'fields':('category', 'sub_category', 'name', 'slug','description', 'status', 'price'),
            
            },
        )
    ]

    def product_count(self, obj):
        return obj.product_set.count()
    