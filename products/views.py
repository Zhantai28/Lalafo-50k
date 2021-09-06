from django import forms
from django.http.response import HttpResponse, Http404
from .models import Category, Product, FeedBack
import django.http as http
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import ProductCreateForm, FeedBackForm
from account.views import * 
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *
from account.models import *


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

        if request.method == "POST":
            product = Product(author=request.user)
            product_form = ProductCreateForm(request.POST, instance=product)
            
            if product_form.is_valid():
                new_product = product_form.save(commit=False)                       
                new_product.author = request.user_id      
                product_form.save()
                return render(request, 'products/user_products.html', {'massages':["Объявление успешно добавлено"]})
            else:
                print(product_form.errors)
        else:
            product_form = ProductCreateForm()
            return render(request, 'products/create.html', {'product_form': product_form})
    else:
        return redirect(register)

class MyProductListView(ListView):
    model = Product
    template_name = 'products/user_products.html'
    
    def get_queryset(self):
        return Product.objects.filter(author__pk__in=[self.request.user.id])
#<<<<   

def edit_my_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product.user_profile != request.user:
        return redirect(register)
    if request.method == "POST":
        product_form = ProductCreateForm(data=request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect(MyProductListView.as_view())
    else:
        form = ProductCreateForm(instance=product)
    return render(request, 'products/editproduct_form.html', {'place_form': form, 'product':product})


def delete_product(request, id):
    product_object = Product.objects.get(id=id)
    product_object.delete()
    return redirect(MyProductListView.as_view())

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



