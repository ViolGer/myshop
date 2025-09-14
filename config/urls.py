from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from config import settings
from products.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL,
               document_root=settings.MEDIA_ROOT))