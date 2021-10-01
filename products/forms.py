from django import forms
from .models import FeedBack, Product


# comments
class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['text',]

 
# Products
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", 'category', "name", "description", "city", "price", 'phone_number', "status"]
    
class ProductActivateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['active']