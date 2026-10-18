from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class CompaniesListView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/list.html'

class BranchListView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/branches.html'