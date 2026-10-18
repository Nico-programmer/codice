from apps.users.mixins import RoleRequiredMixin
from django.views.generic import TemplateView

from django.http import Http404

REPORT_TEMPLATES = {
    'ventas': 'reports/sales.html',
    'compras': 'reports/purchases.html',
    'entradas': 'reports/entries.html',
    'salidas': 'reports/exits.html',
    'ajustes': 'reports/adjustments.html',
    'facturas-electronicas': 'reports/electronic_invoices.html',
}

class ReportDetailView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'contador')
    
    def get_template_names(self):
        template = REPORT_TEMPLATES.get(self.kwargs['report'])
        if template is None:
            raise Http404('Ese reporte no existe')
        return [template]