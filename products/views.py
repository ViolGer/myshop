from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet, Avg
from django.views.generic import DetailView, ListView, TemplateView, FormView
from config.settings import PRODUCT_QUERY_STRING_MAP
from products.forms import ReviewForm
from products.models import Product, Review, Category
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


class ProductDetailView(DetailView):
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    model = Product
    queryset = Product.objects.select_related('category')
    template_name = 'products/product_details.html'
    context_object_name = 'product'

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(is_active=True)
            .select_related('category')
            .prefetch_related('reviews__user')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        context['star_range'] = range(5)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # получаем product
        if not request.user.is_authenticated:
            messages.info(request, "Please sign in to add a review.")
            return redirect(f"{self.object.get_absolute_url()}#reviews")

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = self.object
            review.save()
            messages.success(request, "Thanks for your review!")
            return redirect(f"{self.object.get_absolute_url()}#reviews")

        # если ошибки — показать форму с ошибками
        ctx = self.get_context_data()
        ctx["review_form"] = form
        return self.render_to_response(ctx)


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = (Product.objects
              .filter(is_active=True)
              .select_related("category")
              .prefetch_related("reviews")
              .annotate(avg_rating=Avg('reviews__rating')))

        #filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(category__slug__in=categories.split(','))

        # sort
        order_key = self.request.GET.get('sort', 'new')
        order_by = PRODUCT_QUERY_STRING_MAP.get(order_key, '-created_at')
        qs = qs.order_by(order_by)

        #search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(name__icontains=to_search) |
                Q(description__icontains=to_search)
            )
        return qs



    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paginator = ctx.get("paginator")
        page_obj  = ctx.get("page_obj")
        if paginator and page_obj:
            ctx["elided_page_range"] = paginator.get_elided_page_range(
                number=page_obj.number, on_each_side=1, on_ends=1
            )
        ctx["categories"] = Category.objects.only("name", "slug")
        ctx["current_params"] = self.request.GET.copy()

        return ctx


class ReviewUpsertView(LoginRequiredMixin, FormView):
    form_class = ReviewForm
    template_name = 'products/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug'], is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        existing = Review.objects.filter(product=self.product, user=self.request.user).first()
        if existing:
            initial['rating'] = existing.rating
            initial['comment'] = existing.comment
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['has_my_review'] = (self.request.user.is_authenticated and
                                    Review.objects.filter(product=self.product, user=self.request.user).exists()
                                    )
        return context

    @transaction.atomic
    def form_valid(self, form):
        Review.objects.update_or_create(
            product=self.product,
            user=self.request.user,
            defaults={
                'rating': form.cleaned_data['rating'],
                'comment': form.cleaned_data['comment']
            }
        )
        messages.success(self.request, 'Review saved!')
        return super().form_valid(form)

    def get_success_url(self):
        return f'{self.product.get_absolute_url()}'


class GuidesRecipesView(TemplateView):
    template_name = 'guides-recipes.html'




