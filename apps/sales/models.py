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

class InvoiceNumbering(models.Model):
    branch = models.ForeignKey('companies.Branch', on_delete=models.PROTECT, related_name='invoice_numberings')
    resolution_number = models.CharField(max_length=20, verbose_name="Número de resolución")
    prefix = models.CharField(max_length=10, verbose_name="Prefijo")
    range_from = models.PositiveIntegerField(verbose_name="Desde")
    range_to = models.PositiveIntegerField(verbose_name="Hasta")
    # Arranca en 0; cada factura nueva usa last_number + 1.
    last_number = models.PositiveIntegerField(default=0, verbose_name="Último número usado")
    date_start = models.DateField(verbose_name="Fecha de inicio")
    date_end = models.DateField(verbose_name="Fecha de vencimiento")
    active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f'{self.prefix} ({self.branch})'

    class Meta:
        verbose_name = "Numeración de factura"
        verbose_name_plural = "Numeraciones de factura"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(range_to__gte=models.F('range_from')),
                name='numbering_range_valid',
                violation_error_message='El número "Hasta" debe ser mayor o igual que el "Desde".',
            ),
            models.CheckConstraint(
                condition=models.Q(last_number__lte=models.F('range_to')),
                name='numbering_within_range',
                violation_error_message='Se acabaron los números de esta resolución.',
            ),
            models.CheckConstraint(
                condition=models.Q(date_end__gte=models.F('date_start')),
                name='numbering_dates_valid',
                violation_error_message='La fecha de vencimiento debe ser posterior a la de inicio.',
            ),
        ]