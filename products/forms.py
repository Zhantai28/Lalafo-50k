from django import forms
from .models import Product

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'sub_category', "name", "description", "price", "image", "status"]



