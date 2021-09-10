from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from .views import product_by_category, About, account, register, profile, edit, UserRating, UserRatingView, ChatDetailView, ChatListView, MessagesDetailView, CreateDialogView
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
    path('rate/',UserRatingView.as_view(), name='user-rating'),
    path('chats/', login_required(ChatListView.as_view()), name='dialogs'),
    path('chats/<int:pk>/', login_required(ChatDetailView.as_view()), name='chat_details'),
    path('dialogs/create/<int:user_id>/', login_required(CreateDialogView.as_view()), name='create_dialog'),
    path('dialogs/<user_id>/', login_required(MessagesDetailView.as_view()), name='messages'),
    path('', product_by_category, name='homepage'),
    path('product/<int:id>/', product_by_category, name='product_by_category'),


]

