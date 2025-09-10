from django.contrib import admin
from .models import Cart, CartItem

class CartItemInLine(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'added_at')
    readonly_fields = ['added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'lines', 'quantity', 'total')
    search_fields = ('user__username','user__email')
    readonly_fields = ['created_at']
    inlines = [CartItemInLine]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')
    list_select_related = ('cart__user', 'product')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ['added_at']
