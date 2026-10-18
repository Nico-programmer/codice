from apps.users.mixins import RoleRequiredMixin

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from .forms import CompanyForm, BranchForm
from .models import Branch, Companies

# ============================== Compañias ==============================

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

# ============================== Sucursales ==============================

class BranchScopeMixin:
    """ cada administrado solo ve las sucursales de su empresa; el superusuario ve todas. """

    def get_queryset(self):
        branches = Branch.objects.select_related('company', 'manager').order_by('company__name', 'headquarters')
        if self.request.user.is_superuser:
            return branches
        return branches.filter(company=self.request.user.company)

class BranchFormMixin(BranchScopeMixin):
    model = Branch
    form_class = BranchForm
    template_name = 'companies/branch_form.html'
    success_url = reverse_lazy('companies:branches')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class BranchListView(RoleRequiredMixin, BranchScopeMixin, ListView):
    allowed_roles = ('admin',)
    template_name = 'companies/branches.html'
    context_object_name = 'branches'

class BranchCreateView(RoleRequiredMixin, BranchFormMixin, CreateView):
    allowed_roles = ('admin',)

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.company = self.request.user.company
        messages.success(self.request, f'La sucursal {form.instance.headquarters} quedó creada.')
        return super().form_valid(form)

class BranchUpdateView(RoleRequiredMixin, BranchFormMixin, UpdateView):
    allowed_roles = ('admin',)

    def form_valid(self, form):
        messages.success(self.request, f'Los cambios de {form.instance.headquarters} quedaron guardados.')
        return super().form_valid(form)

class BranchToggleActiveView(RoleRequiredMixin, BranchScopeMixin, View):
    allowed_roles = ('admin',)
    http_method_names = ['post']

    def post(self, request, pk):
        branch = get_object_or_404(self.get_queryset(), pk=pk)
        branch.active = not branch.active
        branch.save(update_fields=['active'])
        status = 'reactivada' if branch.active else 'inactivada'
        messages.success(request, f'La sucursal {branch.headquarters} quedó {status}')
        return redirect('companies:branches')