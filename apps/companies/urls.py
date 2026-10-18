from django.urls import path

from .views import (
    CompaniesListView, CompanyCreateView, CompanyToggleActiveView, CompanyUpdateView,
    BranchListView, BranchCreateView, BranchUpdateView, BranchToggleActiveView
)

app_name = 'companies'

urlpatterns = [
    # Compañias
    path('administracion/empresas/', CompaniesListView.as_view(), name='list'),
    path('administracion/empresas/nueva/', CompanyCreateView.as_view(), name='create'),
    path('administracion/empresas/<int:pk>/editar/', CompanyUpdateView.as_view(), name='update'),
    path('administracion/empresas/<int:pk>/estado/', CompanyToggleActiveView.as_view(), name='toggle_active'),

    # Sucursales
    path('administracion/sucursales/', BranchListView.as_view(), name='branches'),
    path('administracion/sucursales/nueva/', BranchCreateView.as_view(), name='branch_create'),
    path('administracion/sucursales/<int:pk>/editar/', BranchUpdateView.as_view(), name='branch_update'),
    path('administracion/sucursales/<int:pk>/estado/', BranchToggleActiveView.as_view(), name='branch_toggle_active'),
]