from apps.users.mixins import RoleRequiredMixin
from django.views.generic import TemplateView

class HomeView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin', 'vendedor', 'bodeguero', 'contador')
    template_name = 'core/home.html'