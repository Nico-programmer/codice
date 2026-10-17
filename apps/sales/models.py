from django.db import models

from apps.companies.models import Companies

class Customer(models.Model):
    company = models.ForeignKey('companies.Companies', on_delete=models.PROTECT, related_name='customers')

    name = models.CharField(max_length=100, verbose_name="Nombre completo")
    documento_type = models.CharField(max_length=10, choices=Companies.DocumentType.choices, default=Companies.DocumentType.CC, verbose_name="Tipo de documento")
    number_document = models.CharField(max_length=20, verbose_name="Número de documento")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")

    active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f'{self.name} ({self.get_documento_type_display()} {self.number_document})'

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        constraints = [
            models.UniqueConstraint(fields=['company', 'documento_type', 'number_document'], name='unique_customer_document_per_company'),
        ]
