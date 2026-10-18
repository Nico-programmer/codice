from apps.users.mixins import RoleRequiredMixin
from django.views.generic import TemplateView

class CompaniesListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ()
    template_name = 'companies/list.html'

class BranchListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin',)
    template_name = 'companies/branches.html'