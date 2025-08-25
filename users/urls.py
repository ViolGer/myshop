from django.contrib.auth.views import LoginView
from . import views
from django.urls import path

from .views import AccountView

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     redirect_authenticated_user=True,
                                     ), name='login'),
    path('account/', AccountView.as_view(), name='account'),

]