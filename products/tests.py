from django.http import request, response
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from unittest import mock
from .views import add_to_cart, product_by_category
from .models import Product, Category, Cart, CartItem
from account.models import Profile


class ShopTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Книги')
        image = SimpleUploadedFile('book_image.jpg', content=b'', content_type='image/jpg')
        self.book = Product.objects.create(
            category = self.category,
            name = 'book',
            description = 'Test description',
            price = 255,
            image = image,
            status = 'П',
            city = 'Bishkek',
            phone_number = 566527856,

        )

        self.proile = Profile.objects.create(
            user = self.user,
            phone_number = 708566530,
            region = 'B',
            city = 'Bishkek',
        )

        self.cart = Cart.objects.create(owner = self.user)
        self.cart_item = CartItem.objects.create(
            cart = self.cart,
            product = self.book,
        )
    
    def test_add_to_cart(self):
        self.cart.items.add(self.cart_item)
        self.assertIn(self.cart_item, self.cart.items.all())
        self.assertEqual(self.cart.items.count(), 1)
    
        
    def test_list_product_view(self):
        factory = RequestFactory()
        request = factory.get('/account/index')
        request.user = self.user
        response = product_by_category(request)
        self.assertEqual(response.status_code, 200)
    
    def test_create_product(self):
        factory = RequestFactory()
        request = factory.get('/products/create')
        request.user = self.user
        response = product_by_category(request)
        self.assertEqual(response.status_code, 200)