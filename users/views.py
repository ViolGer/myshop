from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from .form import UserRegistrationForm


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/'


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'