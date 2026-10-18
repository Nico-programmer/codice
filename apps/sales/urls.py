from django.urls import path
from .views import NewSaleView, InvoicesListView

app_name = 'sales'

urlpatterns = [
    path('ventas/nueva/', NewSaleView.as_view(), name='new'),
    path('ventas/facturas/', InvoicesListView.as_view(), name='invoices'),
]
