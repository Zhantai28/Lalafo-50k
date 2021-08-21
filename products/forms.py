from django import forms
from django.forms import fields
from .models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ["category", "name", "description", "price", "image", "status"]

