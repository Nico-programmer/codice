from apps.users.mixins import RoleRequiredMixin

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from .forms import CompanyForm
from .models import Branch, Companies

class CompaniesListView(RoleRequiredMixin, ListView):
    allowed_roles = ()
    model = Companies
    template_name = 'companies/list.html'
    context_object_name = 'companies'
    ordering = ['name']

class CompanyCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ()
    model = Companies
    form_class = CompanyForm
    template_name = 'companies/form.html'
    success_url = reverse_lazy('companies:list')

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        Branch.objects.create(
            company=self.object, headquarters='Sede principal',
            address=self.object.address, city=self.object.city, phone=self.object.phone,
        )
        messages.success(self.request, f'La empresa {self.object.name} quedó creada con su sede principal.')
        return response

class CompanyUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ()
    model = Companies
    form_class = CompanyForm
    template_name = 'companies/form.html'
    success_url = reverse_lazy('companies:list')

    def form_valid(self, form):
        messages.success(self.request, f'Los cambios de {form.instance.name} quedaron guardados.')
        return super().form_valid(form)

class CompanyToggleActiveView(RoleRequiredMixin, View):
    allowed_roles = ()
    http_method_names = ['post']

    def post(self, request, pk):
        company = get_object_or_404(Companies, pk=pk)
        company.active = not company.active
        company.save(update_fields=['active'])
        status = 'reactivada' if company.active else 'inactivada'
        messages.success(request, f'La empresa {company.name} quedó {status}.')
        return redirect('companies:list')

class BranchListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin',)
    template_name = 'companies/branches.html'