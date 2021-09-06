from django import views
from django.urls import path
from .views import product_detail, create_product, edit_my_product, delete_product, \
 edit_comment, delete_own_comment, product_by_category, MyProductListView


app_name = 'products'

urlpatterns = [

    # path('feedback/', FeedbackDetailView.as_view(), name='feedback'),
    path('<int:id>/edit/', edit_comment, name='edit-comment'),
    path('<int:id>/delete/', delete_own_comment, name='delete-comment'),
    path('<int:id>/', product_detail, name="product_detail"),
    path('create_product/', create_product, name='create_product'),
    path('user_product/', MyProductListView.as_view(), name='user_products'),
    path('edit/', edit_my_product, name='edit_my_product'),
    path('delete/', delete_product, name='delete_product'),
    path('product-by-category/', product_by_category, name='product_by_category')
]

