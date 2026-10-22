from apps.users.mixins import RoleRequiredMixin

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from .forms import UserCreateForm, UserUpdateForm, is_last_active_admin
from .models import CustomUser

class UserScopeMixin:
    """ Cada administrador solo ve los usuarios de su empresa; el superusuario ve todos (menos otros superusuarios). """

    def get_queryset(self):
        users = CustomUser.objects.filter(is_superuser=False).select_related('company', 'branch').order_by('first_name', 'last_name')
        if self.request.user.is_superuser:
            return users
        return users.filter(company=self.request.user.company)

class UserFormMixin(UserScopeMixin):
    model = CustomUser
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UsersListView(RoleRequiredMixin, UserScopeMixin, ListView):
    allowed_roles = ('admin',)
    template_name = 'users/list.html'
    context_object_name = 'users'

class UserCreateView(RoleRequiredMixin, UserFormMixin, CreateView):
    allowed_roles = ('admin',)
    form_class = UserCreateForm

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.company = self.request.user.company
        messages.success(self.request, f'El usuario {form.instance.username} quedó creado.')
        return super().form_valid(form)

class UserUpdateView(RoleRequiredMixin, UserFormMixin, UpdateView):
    allowed_roles = ('admin',)
    form_class = UserUpdateForm

    def form_valid(self, form):
        messages.success(self.request, f'Los cambios de {form.instance.username} quedaron guardados.')
        return super().form_valid(form)

class UserToggleActiveView(RoleRequiredMixin, UserScopeMixin, View):
    allowed_roles = ('admin',)
    http_method_names = ['post']

    def post(self, request, pk):
        target = get_object_or_404(self.get_queryset(), pk=pk)
        
        if target.pk == request.user.pk:
            messages.error(request, 'No podes inactivar tu propio usuario.')
        elif is_last_active_admin(target):
            messages.error(request, f'{target} es el único administrador activo de su empresa; no se puede inactivar.')
        else:
            target.is_active = not target.is_active
            target.save(update_fields=['is_active'])
            status = 'reactivado' if target.is_active else 'inactivado'
            messages.success(request, f'El usuario {target.username} quedó {status}')
        
        return redirect('users:list')