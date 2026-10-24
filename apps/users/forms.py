from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from apps.companies.forms import capitalize_first
from apps.companies.models import Branch, Companies
from .models import CustomUser

USER_FIELDS = ['first_name', 'last_name', 'username', 'email', 'rol', 'company', 'branch']

def is_last_active_admin(user):
    """ True si el usuario es el único administrador activo de su empresa. """
    if not (user.pk and user.is_active and user.rol == CustomUser.ROL.ADMIN and user.company_id):
        return False

    others = CustomUser.objects.filter(company_id=user.company_id, rol=CustomUser.ROL.ADMIN, is_active=True)
    return not others.exclude(pk=user.pk).exists()

class LoginForm(AuthenticationForm):
    """ El usuario se busca en minúscula: "Juanjose" y "juanjose" son el mismo. """

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()

class UserScopeFormMixin:
    """ Limita empresa y sucursal según quién está llenando el formulario. """

    def setup_scope(self, user):
        self.request_user = user
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        branches = Branch.objects.filter(active=True).select_related('company').order_by('company__name', 'headquarters')
        if user.is_superuser:
            self.fields['company'].queryset = Companies.objects.filter(active=True).order_by('name')
            self.fields['company'].required = True
            self.fields['branch'].queryset = branches.filter(company__active=True)
            self.fields['branch'].label_from_instance = lambda b: f'{b.company.name} · {b.headquarters}'
            self.company = None
        else:
            del self.fields['company'] # El admin de empresa no elige: es la suya
            self.fields['branch'].queryset = branches.filter(company=user.company)
            self.company = user.company

    def clean_first_name(self):
        return capitalize_first(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return capitalize_first(self.cleaned_data['last_name'])

    def clean_username(self):
        username = self.cleaned_data['username'].strip().lower()

        if CustomUser.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ese usuario ya existe. Escribe otro.')
        return username

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean(self):
        cleaned = super().clean()
        company = cleaned.get('company') or self.company
        branch = cleaned.get('branch')
        rol = cleaned.get('rol')

        if company and branch and branch.company_id != company.pk:
            self.add_error('branch', 'Esa sucursal no es de la empresa elegida.')

        email = cleaned.get('email')
        first_name = cleaned.get('first_name')
        last_name = cleaned.get('last_name')

        # El correo es único en todo Codice. Única excepción: un contador que atiende varias empresas
        # (en cada una tiene su usuario, todos con rol contador). En la misma empresa nunca se repite.
        if email:
            taken = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)

            if company and taken.filter(company=company).exists():
                self.add_error('email', 'Ese correo ya lo usa otro usuario de esta empresa.')
            elif taken.exists() and (rol != CustomUser.ROL.CONTADOR or taken.exclude(rol=CustomUser.ROL.CONTADOR).exists()):
                self.add_error('email', 'Ese correo ya lo usa otro usuario de Codice. Solo un contador puede usar el mismo correo en varias empresas.')

        # El nombre completo no se repite dentro de la misma empresa.
        if company and first_name and last_name:
            same_company = CustomUser.objects.filter(company=company).exclude(pk=self.instance.pk)
            if same_company.filter(first_name__iexact=first_name, last_name__iexact=last_name).exists():
                self.add_error('first_name', 'Ya hay un usuario con ese nombre y apellido en esta empresa.')

        # self.instance todavía tiene los datos guardados (antes del cambio)
        if self.instance.pk == self.request_user.pk and rol and rol != self.instance.rol:
            self.add_error('rol', 'No puedes cambiar tu propio rol.')
        elif is_last_active_admin(self.instance):
            if rol and rol != CustomUser.ROL.ADMIN:
                self.add_error('rol', 'Es el único administrador activo de la empresa; no se le puede quitar el rol.')
            if cleaned.get('company') and cleaned['company'].pk != self.instance.company_id:
                self.add_error('company', 'Es el único administrador activo de su empresa; no se puede cambiar de empresa.')
        return cleaned

class UserCreateForm(UserScopeFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = USER_FIELDS

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_scope(user)

class UserUpdateForm(UserScopeFormMixin, forms.ModelForm):
    new_password1 = forms.CharField(label='Nueva contraseña', required=False, strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password2 = forms.CharField(label='Repite la nueva contraseña', required=False, strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    class Meta:
        model = CustomUser
        fields = USER_FIELDS

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get('new_password1')
        password2 = cleaned.get('new_password2')

        # Vacías las dos: no se cambia la contraseña
        if password1 or password2:
            if password1 != password2:
                self.add_error('new_password2', 'Las dos contraseñas no coinciden.')
            else:
                try:
                    password_validation.validate_password(password1, self.instance)
                except forms.ValidationError as error:
                    self.add_error('new_password1', error)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('new_password1'):
            user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_scope(user)