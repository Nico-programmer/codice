from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import UsersListView

app_name = 'users'

urlpatterns = [
    path('ingresar/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True,), name='login'),
    path('salir/', LogoutView.as_view(next_page='users:login'), name='logout'),

    path('administracion/usuarios/', UsersListView.as_view(), name='list'),
]