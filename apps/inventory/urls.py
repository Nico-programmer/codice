from django.urls import path
from .views import ProductListView, ProductCreateView, MovementListView

app_name = 'inventory'

urlpatterns = [
    path('inventario/productos/', ProductListView.as_view(), name='products'),
    path('inventario/productos/nuevo/', ProductCreateView.as_view(), name='product_create'),
    path('inventario/movimientos/', MovementListView.as_view(), name='movements'),
]