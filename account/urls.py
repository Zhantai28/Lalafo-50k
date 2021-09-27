from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from .views import product_by_category, About, account, register, profile, edit, rate_user, Inbox, Directs, NewConversation, SendDirect
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, \
        PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
        PasswordResetDoneView ,PasswordResetConfirmView, PasswordResetCompleteView



app_name = 'account'

urlpatterns = [
    
    path('about-us/', About, name="about_us"),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-then-login/', logout_then_login, name='logout-then-login'),
    path('<int:id>/', account, name='user'),
    path('dashboard/',profile, name='dashboard'), 
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit/', edit, name='edit'),
    path('<int:id>/rate/', rate_user, name='rate-view'),
    path('', product_by_category, name='homepage'),
    path('product/<int:id>/', product_by_category, name='product_by_category'),
    path('message', Inbox, name='inbox'),
    path('message/<username>', Directs, name='directs'),
    path('new/<username>', NewConversation, name='newconversation'),
    path('send/', SendDirect, name='send_direct'),


]

