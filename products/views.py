from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductCreateForm
from account.views import *
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, UpdateView

                                       
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
                return redirect(user_products)
        product_form = ProductCreateForm()
        return render(request, 'products/create.html', {'product_form': product_form})
    else:
        return redirect(register)


def user_products(request):
    data = Product.objects.filter(user_profile=request.user)
    return render(request, 'products/user_products.html', {'user_products': data})


def edit_my_product(request, id):
    if request.method == "POST":
        product_object = Product.objects.filter(user_profile=request.user).get(id=id)
        product_form = ProductCreateForm(data=request.POST, instance=product_object)
        if product_form.is_valid():
            product_form.save()
            return redirect(user_products, id=id)

    product_form = ProductCreateForm(instance=product_form)
    return render(request, 'products/editproduct_form.html', {'place_form': product_form})


def delete_product(request, id):
    product_object = Product.objects.get(id=id)
    product_object.delete()
    return redirect(user_products)
