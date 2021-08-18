from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm,UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


@login_required
def profile(request):
    return render(request, 'account/index.html', {'section': 'profile'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():            
            new_user = user_form.save(commit=False)                       # Create a new user object but avoid saving it yet            
            new_user.set_password(user_form.cleaned_data['password'])     # Set the chosen password
            new_user.save()                                               # Save the User object
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})



@login_required 

def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})




