from django import forms
from django.db import models
from .models import Product
from django.forms import fields

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sub_category', "name", "description", "price", "image", "status"]



