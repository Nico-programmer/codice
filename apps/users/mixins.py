from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(LoginRequiredMixin):
    """ Solo deja entrar a los roles de allowed_roles. El superusuario entra a todo. """

    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser and request.user.rol not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)