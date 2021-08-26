from typing import ForwardRef
from django import forms
from .models import FeedBack 
from django.forms import Textarea


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('product', 'text') 

    def __init__(self, *args, **kwargs):
        super(FeedBackForm).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widjet.attrs['class'] = 'form-control'
        self.fields['text'].widjet = Textarea(attrs={'rows':5})


    