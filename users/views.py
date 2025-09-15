
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from rest_framework.reverse import reverse_lazy

from .form import UserRegistrationForm, UserEditForm


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('products:product_list')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'user_form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/forgot_password.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')