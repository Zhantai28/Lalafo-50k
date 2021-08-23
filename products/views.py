from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product
from .forms import ProductCreateForm
from account.views import *
from account.views import *
# from django.views.generic import FormView, DetailView, CreateView


def product_list(request):
    product_object = Product.objects.all()
    return render(request, 'products/product.html', {"product": product_object})
                                       
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {'product':product})    

# @login_required
def create_product(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(product_detail)
    form = ProductCreateForm()
    return render(request, 'products/create.html', {'product_form': form})

# def product_list(request, cartegory_slug=None):
#     category = None
#     categories_object = Category.objects.all()
#     product_object = Product.objects.all()
#     if cartegory_slug:
#         category = get_object_or_404(Category, slug=cartegory_slug)
#         product_object = product_object.filter(category=category)
#     return render(request, 
#                 'products/product.html', {"category": category,
#                                         "product": product_object,
#                                         "category": categories_object,
#                                         })



                                