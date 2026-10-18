from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class NewSaleView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/new.html'

class InvoicesListView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/invoices.html'