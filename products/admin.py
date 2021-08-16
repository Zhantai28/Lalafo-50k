from django.contrib import admin
from .models import Category, Product, FeedBack 

# class AdminProduct(admin.ModelAdmin):


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'description', 'status', 'price', 'created', 'updated']
    list_filter = ['category', 'status']
    list_editable = ['price', 'status']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(FeedBack) 
