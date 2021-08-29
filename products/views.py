from django.shortcuts import render, redirect
from .models import Category, Product
from .forms import ProductCreateForm
from account.views import *
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *


# from django.views.generic import FormView, DetailView, CreateView


def product_list(request):
    product_object = Product.objects.all()
    return render(request, 'account/index.html', {"product": product_object})
                                       
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
                return redirect(product_list)
        product_form = ProductCreateForm()
        return render(request, 'products/create.html', {'product_form': product_form})
    else:
        return redirect(register)



def user_products(request):
    product = Product.objects.filter(user__gte=1, user__user=request.user)
    return render(request, 'products/user_products.html', {"product": product})



                                