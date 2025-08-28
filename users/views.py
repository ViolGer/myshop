<<<<<<< HEAD
from django.views.generic import CreateView, TemplateView

from users.form import UserRegistrationForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
=======
from django.views.generic import CreateView, FormView, TemplateView

from .form import UserRegistrationForm
>>>>>>> orders


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/'

<<<<<<< HEAD
class AccountView(LoginRequiredMixin, TemplateView):
=======
class AccountView(TemplateView):
>>>>>>> orders
    template_name = 'users/account.html'