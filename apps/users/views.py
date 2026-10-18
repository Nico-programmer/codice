from apps.users.mixins import RoleRequiredMixin
from django.views.generic import TemplateView

class UsersListView(RoleRequiredMixin, TemplateView):
    allowed_roles = ('admin',)
    template_name = 'users/list.html'