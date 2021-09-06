from django import forms
from django.http.response import HttpResponse, Http404
from .models import Category, Product, FeedBack
import django.http as http
from django.views.generic import DetailView, View, ListView
from django.views.generic.edit import FormMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, CartItem, Cart
from .forms import ProductCreateForm, FeedBackForm
from account.views import * 
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *
from account.models import *
from .extras import generate_cart_id






# class FeedbackDetailView(FormMixin, DetailView):
#     template_name = 'products/product_detail.html'
#     form_class = FeedBackForm
#     success_url = '/products/'

#     def post(self, request, *args, **kwargs ):
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.product = self.get_object()
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)
 


def product_detail(request, id):
    product = Product.objects.get(id=id)
    comments = product.product_comments.filter(active=True)

    if request.user.is_authenticated:
        if request.method == 'POST':
            new_comment = comment_form = FeedBackForm(data=request.POST)
            if comment_form.is_valid():
                new_comment.author = request.user
                new_comment = comment_form.save(commit=False)
                new_comment.product = product
                new_comment.save()
                
        else:
            comment_form = FeedBackForm()
        return render(request, 'products/product_detail.html', {'product':product, 
                                                    'comments':comments, 
                                                            'comment_form': comment_form}
                                                            )    
    else:
        return HttpResponse('Только авторизанные пользователи могут оставлять комментарии')


def edit_comment(request, id):
    comment = FeedBack.objects.get(id=id)

    if request.method == 'POST':
        comment_form = FeedBackForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('products/product_detail.html', id=id)

    comment_form = FeedBackForm(instance=comment)
    return render(request, 'products/product_detail.html', {'comment_form': comment_form})


def delete_own_comment(request, id):
    comment = FeedBack.objects.get(id=id)
    comment.delete()
    return redirect('products/product_detail.html')

@login_required 
def create_product(request):
    if request.user.is_authenticated:
        product = Product(author=request.user)

        if request.method == "POST":
            product_form = ProductCreateForm(request.POST, instance=product)
            
            if product_form.is_valid():
                new_product = product_form.save(commit=False)                       
                new_product.author = request.user      
                product_form.save()
                return render(request, 'products/user_products.html', {'massages':["Объявление успешно добавлено"]})
            else:
                print(product_form.errors)
        else:
            product_form = ProductCreateForm(instance=product)
            return render(request, 'products/create.html', {'product_form': product_form})
    else:
        return redirect(register)

class MyProductListView(ListView):
    model = Product
    template_name = 'products/user_products.html'
    
    def get_queryset(self):
        return Product.objects.filter(author__pk__in=[self.request.user.id])

def mypoductdetailview(request, id):
    products = Product.objects.get(id=id)
    return render(request, 'products/detail_user_products.html', {'products':products}) 
        

def edit_my_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product.author != request.user:
        return redirect(register)
    if request.method == "POST":
        edit_form = ProductCreateForm(data=request.POST, instance=product)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(mypoductdetailview)
    else:
        form = ProductCreateForm(instance=product)
    return render(request, 'products/editproduct_form.html', {'product':product})


def delete_product(request, id):
    product_object_delete = Product.objects.get(id=id)
    product_object_delete.delete()
    return redirect(profile)

def product_by_category(request, category_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})



# Cart


def get_user_pending_cart(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Cart.objects.filter(owner=request.user)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def add_to_cart(request, **kwargs):
    
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    # if product in request.user.carts.items.products.all():
    #     messages.info(request, 'You already own this product')
    #     return redirect(reverse('products:product-list')) 
    # create orderItem of the selected product
    user_cart, is_new_cart = Cart.objects.get_or_create(owner=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=user_cart)
    if not created:
        
        messages.info(request, 'This product уже в корзине')
        return redirect(reverse('products:cart_summary'))

        
    if is_new_cart:
        # generate a reference code
        user_cart.ref_code = generate_cart_id()
        user_cart.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('products:cart_summary'))


@login_required()
def delete_from_cart(request, item_id):
    deleted, _ = CartItem.objects.filter(pk=item_id).delete()
    if deleted > 0:
        messages.info(request, "Item has been deleted")
    return redirect(reverse('products:cart_summary'))


@login_required()
def cart_details(request, **kwargs):
    existing_cart = get_user_pending_cart(request)
    context = {
        'order': existing_cart
    }
    return render(request, 'products/cart_summary.html', context)
