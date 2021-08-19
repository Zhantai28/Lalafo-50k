from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from .forms import ProductForm


def product_list(request):
    product_object = Product.objects.all()
    return render(request, 'products/product.html', {"product": product_object})
                                       
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {'product':product})                              

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



                                