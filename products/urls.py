from django import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import product_detail, create_product, edit_my_product, delete_product, \
 edit_comment, delete_own_comment, product_by_category, add_to_cart, delete_from_cart, \
 cart_details, MyProductListView


app_name = 'products'

urlpatterns = [

    # path('feedback/', FeedbackDetailView.as_view(), name='feedback'),
    path('<int:id>/edit/', edit_comment, name='edit-comment'),
    path('<int:id>/delete/', delete_own_comment, name='delete-comment'),
    path('<int:id>/', product_detail, name="product_detail"),
    path('create_product/', create_product, name='create_product'),
    path('<int:id>/edit/', edit_my_product, name='edit_my_product'),
    path('<int:id>/delete/', delete_product, name='delete_product'),

    path('user_product', login_required(MyProductListView.as_view()), name='user_products'),
    path('<int:id>/edit/', edit_my_product, name='edit_my_product'),
    path('<int:id>/delete/', delete_product, name='delete_product'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart-summary/', cart_details, name="cart_summary"),
    path('item/delete/<int:item_id>/', delete_from_cart, name='delete_item'),

    path('product-by-category/', product_by_category, name='product_by_category')
]

