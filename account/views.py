from django.forms.forms import Form
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm,UserEditForm, ProfileEditForm,UserRatingForm, MessageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from .models import Profile, UserRating, Chat, Message
from products.models import Product
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView, DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    QuerySet = Product.objects.all()
    template_name = 'account/index.html'

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
        user_object = User.objects.get(id=id)
        return render(request, 'account/user.html', {'user_object': user_object})
    except User.DoesNotExist as e:
        return HttpResponse(f'Not found: {e}', status=404)



#function for UserRating 


class UserRatingView(LoginRequiredMixin, CreateView):
    template_name = 'account/rating_form.html'
    form_class = UserRatingForm
    success_url = '/account/dashboard/'
        
    def form_valid(self, form):
        form.instance.user_rated = self.request.user
        return super().form_valid(form)



#Message and Chat between users

class ChatListView(ListView):
    model = Chat
    template_name ="account/dialogs.html"

    def get_queryset(self):
        return Chat.objects.filter(members__pk__in=[self.request.user.id])



class ChatDetailView(DetailView):
    template_name ="account/chat_details.html"

    def get_queryset(self):
        return Chat.objects.filter(members__pk__in=[self.request.user.id])


class MessagesDetailView(DetailView):
    def get(self, request, user_id):
        member = User.objects.get(id=user_id)

        try:
            chat_query = Chat.objects.annotate(count=Count('members')).filter(type=Chat.DIALOG, count=2)
            chat_query = chat_query.filter(members__pk = user_id)
            chat_query = chat_query.filter(members__pk = request.user.id)
            chat = chat_query.first()
        except Chat.DoesNotExist:
            chat = None
 
        return render(
            request,
            'account/messages.html',
            {
                'user': request.user,
                'member': member,
                'chat': chat
            }
        )
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('account:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(FormView):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('account:messages', kwargs={'chat_id': chat.id}))




            
            
            
       


