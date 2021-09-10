from django import forms
from django.db.models import fields
from .models import FeedBack, Product
from django.forms import Textarea

# comments
class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['text',]

 
# Products
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', "name", "description", "image", "price", 'phone_number', "status"]
    
