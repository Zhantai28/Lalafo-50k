from typing import ForwardRef
from django import forms
from .models import FeedBack 


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('products', 'text') 