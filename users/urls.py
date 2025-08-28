from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path


app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     redirect_authenticated_user=True,
                                     ), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),

]