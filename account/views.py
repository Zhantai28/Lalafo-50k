from django.forms.forms import Form
from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.template import context, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm,UserEditForm, ProfileEditForm, UserRatingForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from .models import Profile, UserRating, Message
from products.models import Product, Category
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView, DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.template import loader, RequestContext
from django.http import JsonResponse



def product_by_category(request, id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(active=True)
    if id:
        category = get_object_or_404(Category, id=id)
        products = products.filter(category=category)
    return render(request,
                  'account/index.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
        

def About(request):
    if request.method == 'GET':
        return render(request, 'account/aboutus.html')


#profile 

@login_required
def profile(request):
    return render(request, 'account/dashboard.html')

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
            return render(request, 'account/dashboard.html', {'messages': ["Profile updated successfully"]})
        else:
            return HttpResponse("Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

def account(request, id):
    try:
        viewed_user = User.objects.get(profile__id=id)
        product_list = Product.objects.filter(author=viewed_user)
        return render(request, 'account/user.html', {'viewed_user':viewed_user,
                                                    'product_list':product_list})
    except User.DoesNotExist as e:
        return HttpResponse(f'Not found: {e}', status=404)





#function for UserRating 


@login_required
def rate_user(request, id):
    if request.method == 'POST':
        referer = request.META.get('HTTP_REFERER')
        form = UserRatingForm(request.POST)
        if form.is_valid():
            viewed_user=User.objects.get(profile__id=id)
            data = UserRating()
            data.user_rated = request.user
            data.user_received =  viewed_user
            data.rating = form.cleaned_data['rating']
            data.save()
            messages.success(request, "Ваша оценка принята. Благодарим.")
        else:
            print(form.errors)
            messages.error(request, "Произошла ошибка.")
        return HttpResponseRedirect(referer)




# Messaging between users

@login_required
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		}

	template = loader.get_template('account/inbox.html')
	
	return HttpResponse(template.render(context, request))


@login_required
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
	}

	template = loader.get_template('account/inbox.html')

	return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('Неправильный пользователь')
	if from_user != to_user and not Message.objects.filter(user=from_user, recipient=to_user).exists():
		Message.send_message(from_user, to_user, body)
	return redirect('account:inbox')

@login_required
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('account:inbox')
	else:
		HttpResponseBadRequest()

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}