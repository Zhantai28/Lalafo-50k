from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from .forms import ProductForm


def product(request): 
    # cartegory_slug=None):
    # category = None
    # categories_object = Category.objects.all()
    product_object = Product.objects.all()
    # if cartegory_slug:
    #     category = get_object_or_404(Category, slug=cartegory_slug)
    #     product_object = product_object.filter(category=category)
    return render(request, 
                'products/product.html', {"product": product_object})
                                        # "category": categories_object,
                                        # "category": category})
