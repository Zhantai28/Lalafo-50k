from django.urls import path
from django.contrib import admin
from .views import dashboard, register, user_login, edit
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, \
        PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
        PasswordResetDoneView ,PasswordResetConfirmView, PasswordResetCompleteView



app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-then-login/', logout_then_login, name='logout-then-login'),
    path('dashboard/',dashboard, name='dashboard'), 
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit/', edit, name='edit'),
    

]

