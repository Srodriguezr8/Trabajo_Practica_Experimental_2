from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
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
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTO_CHOICES)
    cargo = models.CharField(max_length=50, choices=CARGO_CHOICES)

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

    def clean(self):
        # Valida que el mes sea entre 01 y 12
        if self.aniomes and len(self.aniomes) == 6:
            mes = int(self.aniomes[4:6])
            if not 1 <= mes <= 12:
                raise ValidationError("El mes debe estar entre 01 y 12.")

    def recalcular_totales(self):
        totales = self.detalles.aggregate(
            tot_ing=models.Sum("tot_ing"),
            tot_des=models.Sum("tot_des"),
            neto=models.Sum("neto"),
        )
        self.tot_ing = max(totales["tot_ing"] or Decimal("0"), Decimal("0"))
        self.tot_des = max(totales["tot_des"] or Decimal("0"), Decimal("0"))
        self.neto = max(totales["neto"] or Decimal("0"), Decimal("0"))
        self.save()


class NominaDetalle(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name="detalles")
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iess = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prestamo = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        IESS_RATE = Decimal("0.0945")
        self.tot_ing = max(self.sueldo + self.bono, Decimal("0"))
        self.iess = (self.sueldo * IESS_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.tot_des = max(self.iess + self.prestamo, Decimal("0"))
        self.neto = max((self.tot_ing - self.tot_des).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), Decimal("0"))
        super().save(*args, **kwargs)
        self.nomina.recalcular_totales()
