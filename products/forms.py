from django import forms
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
        fields = ['category', "name", "description", "price", "image", 'phone_number', "status"]

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', "name", "description", "price", "image", 'phone_number', "status")