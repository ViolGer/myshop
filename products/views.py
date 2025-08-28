from django.views.generic import DetailView
from products.models import Product, Review


class ProductDetailView(DetailView):
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    model = Product
    queryset = Product.objects.select_related('category')
    template_name = 'products/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['star_range'] = range(5)
        return context