from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.utils import timezone


class TipoSobretiempo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Ej: "H50", "H100"
    descripcion = models.CharField(max_length=100)
    factor = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Tipo de Sobretiempo"
        verbose_name_plural = "Tipos de Sobretiempo"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Sobretiempo(models.Model):
    empleado = models.ForeignKey('nomina.Empleado', on_delete=models.CASCADE, related_name="sobretiempos")
    fecha_registro = models.DateField(default=timezone.now)
    tipo_sobretiempo = models.ForeignKey(TipoSobretiempo, on_delete=models.CASCADE)
    numero_horas = models.DecimalField(max_digits=6, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal("0.00"))

    HORAS_MENSUALES = Decimal("240.00") 

    class Meta:
        verbose_name = "Sobretiempo"
        verbose_name_plural = "Sobretiempos"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.empleado} - {self.tipo_sobretiempo.codigo} - {self.numero_horas}h"

    def calcular_valor(self):
        sueldo = Decimal(self.empleado.sueldo or Decimal("0.00"))
        factor = Decimal(self.tipo_sobretiempo.factor or Decimal("1.00"))
        horas_mensuales = Decimal(self.HORAS_MENSUALES)
        if horas_mensuales <= 0:
            horas_mensuales = Decimal("240.00")
        bruto = (sueldo / horas_mensuales) * Decimal(self.numero_horas) * factor
        return bruto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        if self.empleado and self.tipo_sobretiempo and self.numero_horas is not None:
            self.valor = self.calcular_valor()
        super().save(*args, **kwargs)
