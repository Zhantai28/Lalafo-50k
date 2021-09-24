from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, UserRating, RATE_CHOICES

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    userbirth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Profile
        fields = ('userbirth', 'phone_number', 'region', 'city', 'photo')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Потвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#Rating Add Form
class UserRatingForm(forms.ModelForm):
   

    
    class Meta:
      model = UserRating
      fields = ['user_received', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        user_rated = cleaned_data.get("user_rated")
        user_received = cleaned_data.get("user_received")

        print(user_rated, user_received)

        if user_rated == user_received:
            raise ValidationError("You can not rate yourself")


