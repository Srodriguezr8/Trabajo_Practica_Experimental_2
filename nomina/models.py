from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal, ROUND_HALF_UP


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

DEPARTAMENTO_CHOICES = (
    ('Ventas', 'Ventas'),
    ('Recursos Humanos', 'Recursos Humanos'),
    ('Marketing', 'Marketing'),
    ('Contabilidad', 'Contabilidad'),
    ('Tecnología', 'Tecnología'),
)

CARGO_CHOICES = (
    ('Gerente', 'Gerente'),
    ('Analista', 'Analista'),
    ('Asistente', 'Asistente'),
    ('Especialista', 'Especialista'),
    ('Desarrollador', 'Desarrollador'),
)

class Empleado(models.Model):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener 10 dígitos')]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[A-Za-z\s]+$', 'El nombre solo puede contener letras y espacios')]
    )
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.CharField(
        max_length=50,
        choices=DEPARTAMENTO_CHOICES
    )
    cargo = models.CharField(
        max_length=50,
        choices=CARGO_CHOICES
    )

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Nomina(models.Model):
    aniomes = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{6}$', 'Formato válido: AAAAMM')]
    )
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Nómina {self.aniomes}"

    def recalcular_totales(self):
        totales = self.detalles.aggregate(
            tot_ing=models.Sum("tot_ing"),
            tot_des=models.Sum("tot_des"),
            neto=models.Sum("neto"),
        )
        self.tot_ing = totales["tot_ing"] or Decimal("0")
        self.tot_des = totales["tot_des"] or Decimal("0")
        self.neto = totales["neto"] or Decimal("0")
        self.save()


class NominaDetalle(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name="detalles")
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iess = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prestamo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        IESS_RATE = Decimal("0.0945")
        self.tot_ing = self.sueldo + self.bono
        self.iess = (self.sueldo * IESS_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.tot_des = self.iess + self.prestamo
        self.neto = (self.tot_ing - self.tot_des).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)
        self.nomina.recalcular_totales()
