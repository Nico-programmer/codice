from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/products.html'

class ProductCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/product_form.html'

class MovementListView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/movements.html'