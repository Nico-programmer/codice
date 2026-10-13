from django.db import models
from django.utils import timezone

class Companies(models.Model):
    class DocumentType(models.TextChoices):
        NIT = 'nit', 'NIT'
        CC = 'cc', 'Cédula de ciudadanía'
        CE = 'ce', 'Cédula de extranjería'

    class PersonType(models.TextChoices):
        JUR = 'juridica', 'Juridica'
        NAT = 'natural', 'Natural'

    document = models.CharField(max_length=30, choices=DocumentType.choices, default=DocumentType.NIT, verbose_name="Documento")
    type_person = models.CharField(max_length=20, choices=PersonType.choices, default=PersonType.NAT, verbose_name="Persona")

    numero_document = models.CharField(max_length=20, verbose_name="# Documento", unique=True)
    name = models.CharField(max_length=50, verbose_name="nombre")
    phone = models.CharField(max_length=14, verbose_name="Telefono") # Incluye el +57
    email = models.EmailField(verbose_name="Correo electronico")

    start_date_subscription = models.DateTimeField(default=timezone.now,verbose_name="Fecha de inicio suscripcion")
    end_date_subscription = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de fin suscripción")

    active = models.BooleanField(default=True, verbose_name="Activa")

    @property
    def subscription_active(self):
        return self.end_date_subscription is not None and self.end_date_subscription >= timezone.now()

    def __str__(self):
        return f'{self.numero_document} - {self.name}'


class Branch(models.Model):
    company = models.ForeignKey("Companies", on_delete=models.PROTECT, related_name="branches")

    headquarters = models.CharField(max_length=100, verbose_name="Sede")
    address = models.CharField(max_length=100, verbose_name="Dirección")
    city = models.CharField(max_length=100, verbose_name="Ciudad")

    active = models.BooleanField(default=True, verbose_name="Activa")

    def __str__(self):
        return self.headquarters