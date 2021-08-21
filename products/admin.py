from django.contrib import admin
from django.db import models
from .models import Category, Product, Subcategory

# class AdminProduct(admin.ModelAdmin):

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 3
    prepopulated_fields = {'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fieldsets = [
        (
            None, {
                'fields':('name', 'slug',)
            }
        )
    ]
    prepopulated_fields = {'slug':('name',)}
        
    inlines = (SubcategoryInline,)

@admin.register(Subcategory)
class SubategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class ProductInline(admin.TabularInline):
    model = Product
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'status', 'price', 'created', 'updated']
    list_filter = ['category', 'status']
    list_editable = ['price', 'status']
    fieldsets = [
        (
            None, {
                'fields':('name', 'slug')
            }
        )
    ]
    inlines = (ProductInline,)
    prepopulated_fields = {'slug':('name',)}

    def product_count(self, obj):
        return obj.product_set.count()
    