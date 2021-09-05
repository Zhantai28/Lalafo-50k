from django import forms
from django.http.response import HttpResponse, Http404
from .models import Category, Product, FeedBack
import django.http as http
from django.views.generic import DetailView, View
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
from .extras import generate_order_id






def product_list(request):
    product_object = Product.objects.all()
    return render(request, 'account/index.html', {'product_list':product_object})



class FeedbackDetailView(FormMixin, DetailView):
    template_name = 'products/feedback.html'
    form_class = FeedBackForm
    success_url = '/products/'

    def post(self, request, *args, **kwargs ):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)



def edit_comment(request, id):
    comment = FeedBack.objects.get(id=id)

    if request.method == 'POST':
        comment_form = FeedBackForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('products/feedback.html', id=id)

    comment_form = FeedBackForm(instance=comment)
    return render(request, 'products/feedback.html', {'comment_form': comment_form})
    


def delete_own_comment(request, id):
    comment = FeedBack.objects.get(id=id)
    comment.delete()
    return redirect('products/feedback.html') 


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {'product':product})    


@login_required 
def create_product(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            product_form = ProductCreateForm(request.POST)
            if product_form.is_valid():
                new_product = product_form.save(commit=False)                       
                new_product.user = request.user      
                product_form.save()
                return render(request, 'products/user_products.html', {'product':new_product})
        product_form = ProductCreateForm()
        return render(request, 'products/create.html', {'product_form': product_form})
    else:
        return redirect(register)

@login_required
def user_products(request):
    if request.method == "GET":
        data = Product.objects.filter(user_profile=request.user)
        return render(request, 'products/user_products.html', {'user_products': data})
    

def edit_my_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_profile != request.user:
        return redirect(register)
    if request.method == "POST":
        product_form = ProductCreateForm(data=request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect(user_products)
    else:
        form = ProductCreateForm(instance=product)
    return render(request, 'products/editproduct_form.html', {'place_form': form, 'product':product})


def delete_product(request, id):
    product_object = Product.objects.get(id=id)
    product_object.delete()
    return redirect(user_products)



# Cart

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Cart.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.mycartproducts.all():
        messages.info(request, 'You already own this product')
        return redirect(reverse('products:product-list')) 
    # create orderItem of the selected product
    order_item, status = CartItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Cart.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('products:product-list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = CartItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('products:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'products/order_summary.html', context)