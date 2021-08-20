from django.urls import path
from .views import FeedbackDetailView, edit_comment, delete_own_comment

app_name = 'products'

urlpatterns = [
    path('feedback/', FeedbackDetailView.as_view(), name='feedback'),
    path('<int:id>/edit/', edit_comment, name='edit-comment'),
    path('<int:id>/delete/', delete_own_comment, name='delete-comment'),
]

