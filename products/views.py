from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import ProductCreateForm
from account.views import * 
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *
from account.models import *

def product_list(request):
    product_object = Product.objects.all()
    return render(request, 'account/index.html', {'product_list':product_object})

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
