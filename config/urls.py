from tempfile import template

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.generic import TemplateView

from config import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('products.urls', namespace='products')),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)