from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add"),
    path("update/<int:product_id>/", views.update_item, name="update"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove"),
    path("clear/", views.clear_cart, name="clear"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/success/", views.CheckoutSuccessView.as_view(), name="checkout_success"),
]
