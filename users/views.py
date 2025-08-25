from django.views.generic import CreateView, FormView

from users.form import UserRegistrationForm, UserLoginForm


class UserCreationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = '/'
