from django.urls import path
from .views import product

app_name = 'products'

urlpatterns = [
    path('product/', product , name="product"),
]

