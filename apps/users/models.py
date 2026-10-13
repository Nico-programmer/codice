from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class ROL(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        VENDEDOR = 'vendedor', 'Vendedor'
        BODEGUERO = 'bodeguero', 'Bodeguero'

    rol = models.CharField(max_length=20, choices=ROL.choices, default=ROL.VENDEDOR)

    company = models.ForeignKey('companies.Companies', on_delete=models.PROTECT, null=True, blank=True, related_name="users")
    branch = models.ForeignKey('companies.Branch', on_delete=models.PROTECT, null=True, blank=True, related_name="users")

    @property
    def iniciales(self):
        return f'{self.first_name[:1]}{self.last_name[:1]}'.upper()

    def __str__(self):
        return self.get_full_name() or self.username