from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from  .models import Cart
from products.models import Product

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': cart.total,
    })

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    qty = int(request.POST.get('qty', 1) or 1)
    qty = max(qty, 1)
    cart.add(product, qty=qty)
    messages.success(request, f'Added to cart: {product.name} (x{qty}).')
    return redirect('cart:cart')

@login_required
@require_POST
def update_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    qty = int(request.POST.get('qty', 1) or 1)
    cart.add(product, qty=qty, replace=True)
    return redirect('cart:cart')

@login_required
@require_POST
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.remove(product)
    messages.info(request, f'Item {product.name} remover from cart.')
    return redirect('cart:cart')

@login_required
@require_POST
def clear_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.clear()
    messages.info(request, 'Cart cleared.')
    return redirect('cart:cart')

def _redirect_back_or_cart(request):

    referer = request.META.get("HTTP_REFERER")

    if referer and request.get_host() in referer:
        return redirect(referer)
    return redirect("cart:cart")


class CheckoutView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        cart = request.session.get("cart", {})
        return render(request, "cart/checkout.html", {"cart": cart})

    def post(self, request):
        request.session["cart"] = {}
        messages.success(request, "Your order has been placed.")
        return redirect("cart:checkout_success")

class CheckoutSuccessView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "cart/checkout_success.html")
