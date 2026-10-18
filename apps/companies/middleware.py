from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

class SubscriptionMiddleware:
    """ Saca del sistema a quien sea de una empresa inactiva o con la suscripción vencida. """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and not user.is_superuser:
            company = user.company
            if company is None or not company.active or not company.subscription_active:
                logout(request)
                messages.error(request, 'La suscripción de tu empresa no está activa. Comunícate con el administrador de tu negocio.')
                return redirect('users:login')
        return self.get_response(request)