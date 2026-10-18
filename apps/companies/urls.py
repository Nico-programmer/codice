from django.urls import path

from .views import (
    BranchListView, CompaniesListView, CompanyCreateView, CompanyToggleActiveView, CompanyUpdateView
)

app_name = 'companies'

urlpatterns = [
    path('administracion/empresas/', CompaniesListView.as_view(), name='list'),
    path('administracion/empresas/nueva/', CompanyCreateView.as_view(), name='create'),
    path('administracion/empresas/<int:pk>/editar/', CompanyUpdateView.as_view(), name='update'),
    path('administracion/empresas/<int:pk>/estado/', CompanyToggleActiveView.as_view(), name='toggle_active'),
    path('administracion/sucursales/', BranchListView.as_view(), name='branches'),
]