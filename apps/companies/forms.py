import re

from django import forms
from django.contrib.auth import get_user_model
from .models import Companies, Branch

DV_WEIGHTS = (3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71)

def nit_verification_digit(nit):
    """ Calcula el dígito de verificación de un NIT con el método de la DIAN. """
    total = sum(int(digit) * weight for digit, weight in zip(reversed(nit), DV_WEIGHTS))
    remainder = total % 11
    return str(remainder if remainder in (0, 1) else 11 - remainder)

def to_upper(value):
    """ Quita espacios de más y deja todo en mayúsculas. """
    return ' '.join(value.split()).upper()

def capitalize_first(value):
    """ Quita espacios de más y pone en mayúscula solo la primera letra. """
    value = ' '.join(value.split())
    return value[:1].upper() + value[1:]

def address_key(value):
    """ Deja solo letras y números, para comparar direcciones escritas de formas distintas. """
    return re.sub(r'[\W_]', '', value.upper())

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = [
            'name', 'legal_name', 'type_person', 'document', 'number_document', 'verification_digit', 'city', 'address', 'phone', 'email', 'start_date_subscription', 'end_date_subscription',
        ]

    def clean_number_document(self):
        number = self.cleaned_data['number_document'].strip()
        if not number.isdigit():
            raise forms.ValidationError('Escribe solo números, sin puntos ni guiones')
        return number

    def clean_name(self):
        return capitalize_first(self.cleaned_data['name'])

    def clean_address(self):
        return to_upper(self.cleaned_data['address'])
    
    def clean_city(self):
        return to_upper(self.cleaned_data['city'])

    def clean(self):
        cleaned = super().clean()
        number = cleaned.get('number_document')
        digit = cleaned.get('verification_digit')
        if cleaned.get('document') == Companies.DocumentType.NIT and number:
            if not digit:
                self.add_error('verification_digit', 'El NIT necesita un dígito de verificación.')
            elif digit != nit_verification_digit(number):
                self.add_error('verification_digit', 'El dígito de verificación no coincide con el NIT.')
        return cleaned

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['company', 'headquarters', 'address', 'city', 'phone', 'manager']

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user.is_superuser:
            self.fields['company'].queryset = Companies.objects.filter(active=True)
            company = self.instance.company if self.instance.pk else None
        else:
            del self.fields['company'] # El admin de empresa no elige: es la suya
            company = user.company
        
        users = get_user_model().objects.filter(is_active=True, company=company)
        self.fields['manager'].queryset = users if company else users.none()
        self.company = company

    def clean_headquarters(self):
        return capitalize_first(self.cleaned_data['headquarters'])

    def clean_address(self):
        return to_upper(self.cleaned_data['address'])

    def clean_city(self):
        return to_upper(self.cleaned_data['city'])

    def clean(self):
        cleaned = super().clean()
        
        company = cleaned.get('company') or self.company
        address = cleaned.get('address')
        city = cleaned.get('city')

        if company and address and city:
            others = Branch.objects.filter(company=company, city__iexact=city).exclude(pk=self.instance.pk)
            if any(address_key(b.address) == address_key(address) for b in others):
                self.add_error('address', 'Ya hay una sucursal de esta empresa en esa dirección.')
        return cleaned