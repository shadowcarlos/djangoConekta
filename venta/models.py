from django.db import models
from django.utils import timezone

# Create your models here.

class PreciosCertificados(models.Model):
    preciocertificado = models.DecimalField(max_digits=5, decimal_places=2)
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.preciocertificado) 


class VentaCertificados(models.Model):
    asociacion = models.CharField(max_length=100 , null=True)
    preciocertificado = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    cantidad = models.IntegerField(null=True)
    tipocambio = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    ivaporcentaje = models.DecimalField(max_digits=4, decimal_places=2,null=True)
    monto = models.DecimalField(default=0, max_digits=9, decimal_places=2,null=True)
    montoiva = models.DecimalField(max_digits=9, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2,null=True)
    creado = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.asociacion  

class Iva(models.Model):
    precioiva = models.DecimalField(max_digits=5, decimal_places=2)
    creado = models.DateTimeField(default=timezone.now, editable=False)
	
    def __str__(self):
        return str(self.precioiva)

class conektaComision(models.Model):
    comision = models.DecimalField(max_digits=5, decimal_places=2)
    creado = models.DateTimeField(default=timezone.now, editable=False)
	
    def __str__(self):
        return str(self.comision)