from django.shortcuts import render
from django.views.generic import CreateView

from users.form import UserRegistrationForm


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/'


