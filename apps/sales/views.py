from django.views.generic import TemplateView
from apps.users.mixins import RoleRequiredMixin

class NewSaleView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'vendedor')
    template_name = 'sales/new.html'

class InvoicesListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'vendedor', 'contador')
    template_name = 'sales/invoices.html'