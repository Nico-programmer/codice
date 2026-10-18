from apps.users.mixins import RoleRequiredMixin
from django.views.generic import TemplateView

class ProductListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'vendedor', 'bodeguero')
    template_name = 'inventory/products.html'

class ProductCreateView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'bodeguero')
    template_name = 'inventory/product_form.html'

class MovementListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'bodeguero')
    template_name = 'inventory/movements.html'