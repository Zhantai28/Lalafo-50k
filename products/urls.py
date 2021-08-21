from django.urls import path
from .views import product_list, product_detail, create_product

# app_name = 'products'

urlpatterns = [
    path('', product_list , name="product_list"),
    path('<int:id>/', product_detail, name="product_detail"),
    path('create_product/', create_product, name='create_product')
]

