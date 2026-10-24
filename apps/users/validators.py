import re

from django.core.exceptions import ValidationError

class SpecialCharacterValidator:
    """ La contraseña debe tener al menos un carácter especial (!@#$%*.-_...). Las letras con tilde y la ñ no cuenta."""

    def validate(self, password, user=None):
        if not re.search(r'[^\w\s]|_', password):
            raise ValidationError('La contraseña debe tener al menos un carácter especial, por ejemplo ! @ # $ % * . -', code='password_no_especial_character',)

    def get_help_text(self):
        return 'Tu contraseña debe tener al menos un carácter especial, por ejemplo ! @ # $ % * . -'