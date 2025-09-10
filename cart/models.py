from django.db import models, transaction
from django.conf import settings
from decimal import Decimal
from django.db.models import F
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart({self.user})'

    #общая сумма
    @property
    def total(self) -> Decimal:
        return sum((item.total_price for item in self.items.select_related('product')), Decimal('0.00'))

    #кол-во позиций
    @property
    def lines(self) -> int:
        return self.items.count()

    #кол-во единиц товара
    @property
    def quantity(self) -> int:
        return self.items.aggregate(q=models.Sum('quantity'))['q'] or 0

    #добавление\изменение кол-ва
    @transaction.atomic
    #чтобы не плодить дубликаты
    def add(self, product: Product, qty: int = 1, replace: bool = False):
        item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if replace:
            item.quantity = max(qty, 0)
        else:
            item.quantity = F('quantity') + qty if not created else qty
        item.save()
        item.refresh_from_db()
        if item.quantity <= 0:
            item.delete()
            return None
        return item

    #удаление позиции
    def remove(self, product: Product):
        self.items.filter(product=product).delete()

    #очистка корзины
    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',

    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'],
                                    name='uniq_cart_product')
        ]

    def __str__(self):
        u = getattr(self.cart, 'user', None)
        uname = getattr(u, 'username', 'anon')
        return f'{self.quantity} x {self.product.name} (for {uname})'

    @property
    def total_price(self) -> Decimal:
        return  (self.product.price or Decimal('0.00')) * self.quantity
