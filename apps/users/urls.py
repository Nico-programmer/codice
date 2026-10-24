from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from .views import UsersListView, UserCreateView, UserUpdateView, UserToggleActiveView

app_name = 'users'

urlpatterns = [
    path('ingresar/', LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm, redirect_authenticated_user=True,), name='login'),
    path('salir/', LogoutView.as_view(next_page='users:login'), name='logout'),

    path('administracion/usuarios/', UsersListView.as_view(), name='list'),
    path('administracion/usuarios/nuevo/', UserCreateView.as_view(), name='create'),
    path('administracion/usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='update'),
    path('administracion/usuarios/<int:pk>/estado/', UserToggleActiveView.as_view(), name='toggle_active'),
]