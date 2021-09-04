from django import views
from django.urls import path
from .views import product_detail, create_product, edit_my_product, delete_product, \
FeedbackDetailView, edit_comment, delete_own_comment, user_products


app_name = 'products'

urlpatterns = [
    #feedback for products
    path('feedback/', FeedbackDetailView.as_view(), name='feedback'),
    path('<int:id>/edit/', edit_comment, name='edit-comment'),
    path('<int:id>/delete/', delete_own_comment, name='delete-comment'),

    #products
    path('<int:id>/', product_detail, name="product_detail"),
    path('create_product/', create_product, name='create_product'),
    path('user_product', user_products, name='user_products'),
    path('<int:id>/edit/', edit_my_product, name='edit_my_product'),
    path('<int:id>/delete/', delete_product, name='delete_product'),

]

