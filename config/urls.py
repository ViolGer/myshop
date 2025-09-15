from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from config import settings
from products.views import ProductListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL,
               document_root=settings.MEDIA_ROOT))

urlpatterns += [
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]