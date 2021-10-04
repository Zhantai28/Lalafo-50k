from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_http_methods
from .models import Product, FeedBack 
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, CartItem, Cart
from .forms import ProductCreateForm, FeedBackForm, ProductActivateForm
from account.views import * 
from account.forms import *
from django.contrib.auth.decorators import login_required
from account.templates import *
from account.models import *
from .extras import generate_cart_id 
from django.contrib import auth


def product_detail(request, id):
    product = Product.objects.get(id=id)
    comments = FeedBack.objects.filter(product=id)
    context = {'product':product, 
                    'comments':comments}
    return render(request, 'products/product_detail.html', context=context)



@login_required(login_url='/login/')
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment_form = FeedBackForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = product
            comment_form.save() 
            return redirect(product)
        else:
            return HttpResponse('Содержание формы неверно, пожалуйста, заполните его.')
        
    else:
        return HttpResponse("Публиковать комментарии принимаются только запросы POST.") 

        
                                                             
def delete_own_comment(request, id):
    comment, _ = FeedBack.objects.filter(id=id).delete()
    if comment:
        messages.info(request, "Item has been deleted")
    return redirect(reverse('products:user_products'))



# Product

@login_required 
def create_product(request):
    product = Product(author=request.user)

    if request.method == "POST":
        product_form = ProductCreateForm(request.POST, instance=product, files=request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)                       
            new_product.author = request.user      
            product_form.save()
            return redirect(reverse('products:user_products'))
        else:
            print(product_form.errors)
    else:
        product_form = ProductCreateForm(instance=product)
        return render(request, 'products/create.html', {'product_form': product_form})



def search_products(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    search_products = Product.objects.filter(name__icontains=q).filter(active=True)
    context = {'search_products': search_products}
    return render(request, 'account/index.html', context)


    

def edit_my_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        edit_form = ProductCreateForm(data=request.POST, instance=product, files=request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('products:user_products'))
    else:
        edit_form = ProductCreateForm(instance=product)
    return render(request, 'products/editproduct_form.html', {'product':product, 
                                                            "edit_form":edit_form})


def delete_product(request, id):
    deleted, _ = Product.objects.filter(pk=id).delete()
    if deleted > 0:
        messages.info(request, "Item has been deleted")
    return redirect(reverse('products:user_products'))



class MyProductListView(ListView):
    model = Product
    template_name = 'products/user_products.html'
    
    def get_queryset(self):
        return Product.objects.filter(author__pk__in=[self.request.user.id]).filter(active=True)

    
class MyArchiveProducts(ListView):
    model = Product
    template_name = 'products/user_products.html'
    
    def get_queryset(self):
        return Product.objects.filter(author__pk__in=[self.request.user.id]).filter(active=False)
        

def mypoductdetailview(request, id):
    products = Product.objects.get(id=id)
    comments = FeedBack.objects.filter(product=id)
    if request.method == "POST":
        deactivation_form = ProductActivateForm(data=request.POST, instance=products)
        if deactivation_form.is_valid():
            deactivation_form.save()
            return redirect(reverse('products:user_products'))
    else:
       deactivation_form = ProductActivateForm(instance=products)
    return render(request, 'products/detail_user_products.html', {'products':products, 'form':deactivation_form, 'comments':comments}) 
        

class MyProductCommentsListView(ListView):
    model = FeedBack
    template_name = 'products/detail_user_products.html'
    
    def get_queryset(self):
        return FeedBack.objects.filter(feedback__pk__in=[self.request.user.id])





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
