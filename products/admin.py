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



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['text', 'product', 'user']
    search_fields = ['text', 'product__name', 'product__description']
    fields = ['user', 'product', 'text']
    readonly_fields = ['product', 'text']

admin.site.register(FeedBack, FeedbackAdmin) 
