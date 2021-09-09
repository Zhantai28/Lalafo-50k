from django import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import product_detail, create_product, edit_my_product, delete_product, \
 delete_own_comment, product_by_category, add_to_cart, delete_from_cart, \
 cart_details, MyProductListView, mypoductdetailview, MyProductCommentsListView


app_name = 'products'

urlpatterns = [

    path('<int:id>/delete-comment/', delete_own_comment, name='delete-comment'),
    path('user_product_comments', MyProductCommentsListView.as_view(), name='my-product-comments'),

    path('<int:id>/', product_detail, name="product_detail"),
    path('create_product/', create_product, name='create_product'),
    path('edit-product/<int:id>/', edit_my_product, name='edit_my_product'),
    path('<int:id>/delete-product/', delete_product, name='delete_product'),
    path('user_product/<int:id>/', mypoductdetailview, name='my-product-detail'),

    path('user_product', login_required(MyProductListView.as_view()), name='user_products'),
    path('<int:id>/edit/', edit_my_product, name='edit_my_product'),
    path('<int:id>/delete/', delete_product, name='delete_product'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart-summary/', cart_details, name="cart_summary"),
    path('item/delete/<int:item_id>/', delete_from_cart, name='delete_item'),

    path('product-by-category/', product_by_category, name='product_by_category')
]

