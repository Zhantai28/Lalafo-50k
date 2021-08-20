from django import forms
from django.http.response import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from .models import Category, Product, FeedBack
import django.http as http
from .forms import FeedBackForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.template import RequestContext




class FeedbackDetailView(FormMixin, DetailView):
    template_name = 'products/feedback.html'
    form_class = FeedBackForm
    success_url = '/products/'

    def post(self, request, *args, **kwargs ):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)



def edit_comment(request, id):
    comment = FeedBack.objects.get(id=id)

    if request.method == 'POST':
        comment_form = FeedBackForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect('products/feedback.html', id=id)

    comment_form = FeedBackForm(instance=comment)
    return render(request, 'products/feedback.html', {'comment_form': comment_form})
    


def delete_own_comment(request, id):
    comment = FeedBack.objects.get(id=id)
    comment.delete()
    return redirect('products/feedback.html') 

