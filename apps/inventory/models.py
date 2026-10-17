from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    class IvaRate(models.IntegerChoices):
        CERO = 0, '0%'
        REDUCIDO = 5, '5%'
        GENERAL = 19, '19%'

    company = models.ForeignKey('companies.Companies', on_delete=models.PROTECT, related_name='products')
    code = models.CharField(max_length=50, verbose_name="Código")
    name = models.CharField(max_length=150, verbose_name="Nombre")
    price = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)], verbose_name="Precio")
    iva = models.PositiveSmallIntegerField(choices=IvaRate.choices, default=IvaRate.GENERAL, verbose_name="Iva")
    min_stock = models.IntegerField(default=5, validators=[MinValueValidator(0)], verbose_name="Cantidad minima")
    active = models.BooleanField(default=True, verbose_name="Activo")

    @property
    def total_stock(self):
        return self.stocks.aggregate(total=models.Sum('quantity'))['total'] or 0

    def __str__(self):
        return f'{self.code}: {self.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'code'], name='unique_code_per_company'),
            models.CheckConstraint(condition=models.Q(price__gte=0), name='price_not_negative'),
            models.CheckConstraint(condition=models.Q(min_stock__gte=0), name='min_stock_not_negative'),
        ]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stocks')
    branch = models.ForeignKey('companies.Branch', on_delete=models.PROTECT, related_name='stocks')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Cantidad")

    def __str__(self):
        return f'{self.product} en {self.branch}: {self.quantity}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'branch'], name='unique_stock_per_branch'),
            models.CheckConstraint(condition=models.Q(quantity__gte=0), name='stock_not_negative'),
        ]
        verbose_name = 'Existencia'
        verbose_name_plural = 'Existencias'