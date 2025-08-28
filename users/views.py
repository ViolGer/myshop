from django.views.generic import CreateView, TemplateView

from users.form import UserRegistrationForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/'

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'