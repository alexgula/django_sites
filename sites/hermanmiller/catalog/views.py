# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from picassoft.utils.classviews import JSONResponseMixin
from navigation.views import HomeNavigationView, NavigationListView, NavigationDetailView, NavigationTreeDetailView
from navigation.models import StaticNode
from .models import Category, Product, ProductReview
from shop import session
from . import email


class CategoryListView(NavigationListView):
    model = Category
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Catalog"), 'category_list')
    queryset = Category.objects.order_by('title').prefetch_related('products').all()


class CategoryDetailView(NavigationTreeDetailView):
    model = Category
    trail_parent = CategoryListView


class ProductDetailView(NavigationDetailView):
    model = Product
    trail_parent = CategoryDetailView

    def get_trail_nodes(self):
        trail = super(NavigationDetailView, self).get_trail_nodes()
        return trail + [self.object.category, self.object]

    def get_queryset(self):
        return Product.objects.select_related('category').filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        customer = session.auth.get_data(self.request)
        if customer is not None:
            context['review_author'] = customer.name
            context['review_email'] = customer.email

        return context


class ProductReviewView(View, JSONResponseMixin):
    def post(self, request, *args, **kwargs):
        product = Product.objects.select_related('category')\
            .filter(category__slug=self.kwargs['category_slug']).get(slug=self.kwargs['slug'])
        review = ProductReview(
            product=product,
            author=self.request.POST['author'],
            email=self.request.POST['email'],
            text=self.request.POST['text']
        )
        review.save()
        email.send_review_notification(self.request, review)
        return self.render_to_response({'result': 'success'})
