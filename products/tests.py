import unittest
from django.http import response
from django.test import TestCase
from products.models import Product
from django.urls import reverse
from .urls import create_product

class ProductCreateTestCase(unittest.TestCase):
    def test_create_product_success(self):
        url = reverse("create_product", args=['1'])
        data = {
            'name': 'Стол',
            'price': 250,
            'description':'Большой круглый стол',
        }
        self.response = self.client.post(url, data)
        product = Product.objects.first()
        self.assertEqual(product.name, 'Стол')    