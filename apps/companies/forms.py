from django import forms
from .models import Companies

DV_WEIGHTS = (3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71)

def nit_verification_digit(nit):
    """ Calcula el dígito de verificación de un NIT con el método de la DIAN. """
    total = sum(int(digit) * weight for digit, weight in zip(reversed(nit), DV_WEIGHTS))
    remainder = total % 11
    return str(remainder if remainder in (0, 1) else 11 - remainder)

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