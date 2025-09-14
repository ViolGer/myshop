from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .views import UserCreateView, AccountView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     next_page=reverse_lazy('users:home'),
                                     ), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('cart/', TemplateView.as_view(template_name='users/cart.html'), name='cart'),

]