from django.db import models
from django.conf import settings

from apps.companies.models import Companies
from apps.inventory.models import Product

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

class Sale(models.Model):
    class InvoiceType(models.TextChoices):
        NOR = 'nor', 'Normal'
        ELC = 'elc', 'Electrónica'

    class StatusType(models.TextChoices):
        PEN = 'pen', 'Pendiente'
        EMI = 'emi', 'Emitida'
        REC = 'rec', 'Rechazada'
    
    company = models.ForeignKey('companies.Companies', on_delete=models.PROTECT, related_name='sales')
    branch = models.ForeignKey('companies.Branch', on_delete=models.PROTECT, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sales')
    numbering = models.ForeignKey(InvoiceNumbering, on_delete=models.PROTECT, related_name='sales')

    number = models.PositiveIntegerField(verbose_name="Número")
    type = models.CharField(max_length=20, choices=InvoiceType.choices, default=InvoiceType.NOR, verbose_name="Tipo")
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.EMI, verbose_name="Estado")
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Subtotal")
    iva = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="IVA")
    total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Total")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return f'{self.numbering.prefix}-{self.number}'

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        constraints = [
            models.UniqueConstraint(fields=['numbering', 'number'], name='unique_invoice_number_per_numbering'),
        ]

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT, related_name='sale_items')

    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    # Precio e IVA copiados del producto el día de la venta: si el producto cambia después, la factura no.
    unit_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Precio unitario")
    iva_rate = models.PositiveSmallIntegerField(choices=Product.IvaRate.choices, verbose_name="Tarifa de IVA")
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Subtotal")
    iva = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="IVA")
    total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Total")

    def __str__(self):
        return f'{self.sale} - {self.product}'

    class Meta:
        verbose_name = "Producto vendido"
        verbose_name_plural = "Productos vendidos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name='sale_item_quantity_positive',
                violation_error_message='La cantidad debe ser mayor que 0.',
            ),
        ]