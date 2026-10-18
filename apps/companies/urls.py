from django.urls import path

from .views import CompaniesListView, BranchListView

app_name = 'companies'

urlpatterns = [
    path('administracion/empresas/', CompaniesListView.as_view(), name='list'),
    path('administracion/sucursales/', BranchListView.as_view(), name='branches'),
]