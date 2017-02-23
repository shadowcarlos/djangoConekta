from django.contrib import admin
from .models import PreciosCertificados, VentaCertificados, Iva, conektaComision
# Register your models here.
admin.site.register(PreciosCertificados)
admin.site.register(VentaCertificados)
admin.site.register(Iva)
admin.site.register(conektaComision)